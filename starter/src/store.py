"""Store and search vectors using PostgreSQL + pgvector."""
from typing import Any
import json
import psycopg
from .models import Chunk


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int = 768) -> None:
        """Retain connection settings; validate model dimensions."""
        self.database_url = database_url
        self.dimensions = dimensions
        if not (1 <= dimensions <= 2000):
            raise ValueError(f"Invalid dimensions {dimensions} for pgvector index.")

    def _get_connection(self):
        return psycopg.connect(self.database_url)

    def create_schema(self) -> None:
        """Create table with vector column and source/page/filter metadata."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS chunks (
                        strategy VARCHAR(50) NOT NULL,
                        chunk_id VARCHAR(255) NOT NULL,
                        document_id VARCHAR(255) NOT NULL,
                        source TEXT NOT NULL,
                        page INTEGER NOT NULL,
                        text TEXT NOT NULL,
                        metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                        embedding vector({self.dimensions}) NOT NULL,
                        PRIMARY KEY (strategy, chunk_id)
                    );
                    CREATE INDEX IF NOT EXISTS idx_chunks_strategy ON chunks (strategy);
                    CREATE INDEX IF NOT EXISTS idx_chunks_metadata ON chunks USING gin (metadata);
                """)
            conn.commit()

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Validate lengths/dimensions and write stable IDs without duplicates.

        When re-ingesting changed source documents, remove obsolete chunks too.
        """
        if len(chunks) != len(vectors):
            raise ValueError(f"Mismatch: {len(chunks)} chunks vs {len(vectors)} vectors.")

        for v in vectors:
            if len(v) != self.dimensions:
                raise ValueError(f"Vector dimension {len(v)} does not match store dimension {self.dimensions}.")

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                # Delete existing chunks for this strategy to avoid stale or obsolete chunks
                cur.execute("DELETE FROM chunks WHERE strategy = %s;", (strategy,))
                
                # Bulk insert using executemany
                insert_sql = """
                    INSERT INTO chunks (strategy, chunk_id, document_id, source, page, text, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s::vector)
                    ON CONFLICT (strategy, chunk_id) DO UPDATE SET
                        document_id = EXCLUDED.document_id,
                        source = EXCLUDED.source,
                        page = EXCLUDED.page,
                        text = EXCLUDED.text,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding;
                """
                records = []
                for chunk, vector in zip(chunks, vectors):
                    vec_str = "[" + ",".join(f"{x:.6f}" for x in vector) + "]"
                    meta_str = json.dumps(chunk.metadata, ensure_ascii=False)
                    records.append((
                        strategy,
                        chunk.chunk_id,
                        chunk.document_id,
                        chunk.source,
                        chunk.page,
                        chunk.text,
                        meta_str,
                        vec_str
                    ))
                cur.executemany(insert_sql, records)
            conn.commit()

    def search(self, strategy: str, query_vector: list[float], top_k: int = 3,
               filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Filter permitted metadata in SQL, rank by cosine distance, return top-k.

        Return chunk ID, text, score and metadata. Parameterize user-supplied values.
        """
        if len(query_vector) != self.dimensions:
            raise ValueError(f"Query vector dimension {len(query_vector)} != {self.dimensions}")

        query_vec_str = "[" + ",".join(f"{x:.6f}" for x in query_vector) + "]"

        # Base SQL query
        where_clauses = ["strategy = %s"]
        params: list[Any] = [query_vec_str, strategy]

        if filters:
            for k, v in filters.items():
                where_clauses.append("metadata->>%s = %s")
                params.extend([str(k), str(v)])

        where_sql = " AND ".join(where_clauses)
        params.extend([query_vec_str, top_k])

        sql = f"""
            SELECT chunk_id, document_id, source, page, text, metadata,
                   1.0 - (embedding <=> %s::vector) AS score
            FROM chunks
            WHERE {where_sql}
            ORDER BY embedding <=> %s::vector ASC
            LIMIT %s;
        """

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()

        results = []
        for row in rows:
            meta = row[5]
            if isinstance(meta, str):
                meta = json.loads(meta)
            results.append({
                "chunk_id": row[0],
                "document_id": row[1],
                "source": row[2],
                "page": row[3],
                "text": row[4],
                "metadata": meta,
                "score": float(row[6])
            })
        return results
