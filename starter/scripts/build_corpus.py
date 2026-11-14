import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors

data_dir = Path(__file__).resolve().parents[1] / "data"
data_dir.mkdir(parents=True, exist_ok=True)
pdf_path = data_dir / "vinuni_academic_handbook_2025_2026.pdf"

doc = SimpleDocTemplate(
    str(pdf_path),
    pagesize=letter,
    leftMargin=54,
    rightMargin=54,
    topMargin=54,
    bottomMargin=54,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Title"],
    fontSize=22,
    leading=26,
    textColor=colors.HexColor("#0f2a4a"),
    alignment=1,
)

subtitle_style = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontSize=13,
    leading=17,
    textColor=colors.HexColor("#334d6e"),
    alignment=1,
)

heading1_style = ParagraphStyle(
    "SectionHeading",
    parent=styles["Heading1"],
    fontSize=15,
    leading=19,
    textColor=colors.HexColor("#0f2a4a"),
    spaceAfter=10,
)

heading2_style = ParagraphStyle(
    "SubSectionHeading",
    parent=styles["Heading2"],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#1b4b7a"),
    spaceAfter=6,
)

body_style = ParagraphStyle(
    "BodyTextCustom",
    parent=styles["BodyText"],
    fontSize=10,
    leading=14,
    textColor=colors.HexColor("#222222"),
    spaceAfter=8,
)

callout_style = ParagraphStyle(
    "CalloutText",
    parent=styles["Normal"],
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor("#0f2a4a"),
    backColor=colors.HexColor("#f0f4f8"),
    borderColor=colors.HexColor("#cbdbe8"),
    borderWidth=1,
    borderPadding=6,
    spaceAfter=8,
)

story = []

# ==========================================
# PAGE 1: COVER PAGE (Excluded from content)
# ==========================================
story.append(Spacer(1, 100))
story.append(Paragraph("VINUNIVERSITY", title_style))
story.append(Spacer(1, 15))
story.append(Paragraph("ACADEMIC REGULATIONS &amp; STUDENT POLICY HANDBOOK", title_style))
story.append(Spacer(1, 15))
story.append(Paragraph("Academic Year 2025 - 2026 | Effective Date: August 15, 2025", subtitle_style))
story.append(Spacer(1, 20))
story.append(Paragraph("Office of the University Registrar &amp; Academic Affairs<br/>Vinhomes Ocean Park, Gia Lam, Hanoi, Vietnam", subtitle_style))
story.append(Spacer(1, 150))
story.append(Paragraph("Document Classification: Official University Policy (Public)<br/>Version: 2025.2 | Document ID: VINUNI-HANDBOOK-2025", subtitle_style))
story.append(PageBreak())

# ==========================================
# PAGE 2: TABLE OF CONTENTS (Excluded from content)
# ==========================================
story.append(Paragraph("TABLE OF CONTENTS", heading1_style))
story.append(Spacer(1, 10))
toc_items = [
    ("Section 1: Undergraduate Admissions &amp; Matriculation", "Pages 3 - 6"),
    ("Section 2: Course Registration, Credit Limits &amp; Course Changes", "Pages 7 - 10"),
    ("Section 3: Class Attendance, Leave of Absence &amp; Withdrawal", "Pages 11 - 14"),
    ("Section 4: Grading System, GPA Calculation &amp; Grade Appeals", "Pages 15 - 18"),
    ("Section 5: Academic Standing, Warning &amp; Dismissal", "Pages 19 - 22"),
    ("Section 6: Academic Integrity, Misconduct &amp; Disciplinary Code", "Pages 23 - 26"),
    ("Section 7: Degree Requirements, Graduation &amp; Latin Honors", "Pages 27 - 30"),
    ("Section 8: Tuition Schedule, Scholarships &amp; Financial Aid", "Pages 31 - 35"),
    ("Appendix &amp; Index of Regulatory Terms", "Page 36"),
]
for title, pgs in toc_items:
    story.append(Paragraph(f"<b>{title}</b> .................................................... {pgs}", body_style))
    story.append(Spacer(1, 4))
story.append(PageBreak())

# ==========================================
# PAGES 3 - 6: SECTION 1 - ADMISSIONS
# ==========================================
# Page 3
story.append(Paragraph("Section 1: Undergraduate Admissions &amp; Matriculation", heading1_style))
story.append(Paragraph("1.1 General Admissions Standards and Holistic Review", heading2_style))
story.append(Paragraph("VinUniversity undergraduate admissions employs a comprehensive holistic assessment framework designed to evaluate intellectual capability, personal character, and leadership aspiration. Every application is independently reviewed by members of the Admissions Committee across four core dimensions: Academic Excellence, Leadership Potential, Creative Thinking, and Inherent Passion.", body_style))
story.append(Paragraph("Applicants must have completed recognized secondary education equivalent to high school graduation in Vietnam or international curricula (including IB Diploma, Cambridge A-Levels, or Advanced Placement credentials). The minimum secondary cumulative grade point average required for consideration is 7.5 on a 10.0 scale, or 3.0 on a 4.0 scale.", body_style))
story.append(Paragraph("All application packages must include verified high school transcripts for grades 10, 11, and 12, standardized test scores (if applicable), two confidential letters of recommendation from secondary school teachers or counselors, and a personal statement between 500 and 700 words addressing the candidate's life motivations and community impact goals.", body_style))
story.append(Paragraph("Special consideration is given to national Olympiad medalists and candidates demonstrating extraordinary entrepreneurial or social service achievements, subject to ratification by the Academic Council.", body_style))
story.append(PageBreak())

# Page 4
story.append(Paragraph("Section 1: Undergraduate Admissions &amp; Matriculation", heading1_style))
story.append(Paragraph("1.2 English Language Proficiency Prerequisites", heading2_style))
story.append(Paragraph("Because the official medium of instruction and academic research across all colleges at VinUniversity is English, candidates must substantiate adequate linguistic competence prior to formal matriculation into credit-bearing coursework.", body_style))
story.append(Paragraph("The standard baseline English qualification for unconditional admission is an overall band score of at least 6.5 on the International English Language Testing System (IELTS Academic), with no individual sub-band score falling below 6.0 in Listening, Reading, Writing, and Speaking. Equivalently, a score of 79 on the Test of English as a Foreign Language internet-based test (TOEFL iBT) with minimum section scores of 19, or a Pearson Test of English Academic (PTE Academic) score of 58 is accepted.", body_style))
story.append(Paragraph("Exemption from English testing is granted strictly to candidates whose native language is English, or those who have successfully completed three consecutive years of secondary instruction in a school where English is the sole instructional language, supported by official accreditation documentation.", body_style))
story.append(Paragraph("Applicants presenting an IELTS score between 5.5 and 6.0 are granted provisional admission conditional upon mandatory enrollment in the Pathway English Immersion Program during the summer prior to the fall semester.", body_style))
story.append(PageBreak())

# Page 5
story.append(Paragraph("Section 1: Undergraduate Admissions &amp; Matriculation", heading1_style))
story.append(Paragraph("1.3 Application Rounds, Deadlines, and Evaluative Interview", heading2_style))
story.append(Paragraph("The annual undergraduate admissions cycle comprises three sequential evaluation windows: the Early Decision Round, the Regular Decision Round, and the Rolling Admissions Round. Applicants are strongly advised to submit documentation during earlier windows to optimize merit scholarship consideration.", body_style))
story.append(Paragraph("For the 2025-2026 academic year, the deadline for the Early Decision Round is November 15, 2025; the Regular Decision Round closes on March 15, 2026; and the final Rolling Admissions Round concludes on May 31, 2026. Submissions past 23:59 Indochina Time (UTC+7) on the respective deadline dates will not be reviewed for that cycle.", body_style))
story.append(Paragraph("Shortlisted candidates must complete a 30-minute interactive evaluative interview conducted in English by a dual-member faculty panel. The interview assesses problem-solving methodology, ethical reasoning, collaborative mindset, and alignment with the university's core institutional values: EXCEL (Empathy, Exception, Creativity, Entrepreneurship, Leadership).", body_style))
story.append(Paragraph("Interview performance contributes 35% of the composite score used in final admission and scholarship allocation determinations.", body_style))
story.append(PageBreak())

# Page 6
story.append(Paragraph("Section 1: Undergraduate Admissions &amp; Matriculation", heading1_style))
story.append(Paragraph("1.4 Enrollment Confirmation, Deposit and Document Verification", heading2_style))
story.append(Paragraph("Successful applicants receive an official Offer of Admission issued electronically by the Office of the University Registrar. To secure a seat in the matriculating cohort, admitted students must complete formal acceptance within 14 calendar days of offer transmission.", body_style))
story.append(Paragraph("A non-refundable enrollment deposit of 20,000,000 VND is required upon acceptance. This deposit is credited in full toward the first semester's tuition liability but is forfeited should the admitted candidate decline enrollment subsequent to confirmation.", body_style))
story.append(Paragraph("Matriculation is contingent upon physical verification of original diplomas, apostilled transcripts, medical clearance records confirming immunization compliance, and valid identification. Falsification or withholding of academic history constitutes grounds for immediate revocation of admission and permanent disqualification from future university programs.", body_style))
story.append(Paragraph("All verified new students must participate in the mandatory New Student Orientation Week commencing exactly one week prior to the start of classes in the Fall Semester.", body_style))
story.append(PageBreak())

# ==========================================
# PAGES 7 - 10: SECTION 2 - REGISTRATION
# ==========================================
# Page 7
story.append(Paragraph("Section 2: Course Registration &amp; Credit Limits", heading1_style))
story.append(Paragraph("2.1 Academic Credit Framework and Term Workload Limits", heading2_style))
story.append(Paragraph("Academic progression at VinUniversity is measured in United States semester credit units. One lecture credit corresponds to 15 contact hours of classroom instruction plus an expected 30 hours of supplementary student preparation, analysis, and study over the semester. Laboratory, clinical, and studio credits require a minimum of 30 to 45 contact hours per credit.", body_style))
story.append(Paragraph("Undergraduate degree candidates must maintain full-time academic status by registering for a minimum of 12 credit units in both the Fall and Spring semesters. The standard semester academic workload is 15 to 18 credit units, representing 4 to 5 major courses.", body_style))
story.append(Paragraph("The maximum allowable credit enrollment without special authorization is 20 credit units per standard 15-week semester. During the optional Summer Term (8 weeks), the maximum allowable credit load is 8 credit units, representing no more than two intensive academic courses.", body_style))
story.append(Paragraph("Registration below 12 credit units triggers part-time status, which requires prior approval from the Dean of College and may result in the forfeiture of merit scholarships and residential housing privileges.", body_style))
story.append(PageBreak())

# Page 8
story.append(Paragraph("Section 2: Course Registration &amp; Credit Limits", heading1_style))
story.append(Paragraph("2.2 Overload Credit Approval Criteria and Procedures", heading2_style))
story.append(Paragraph("Enrolling in academic credit beyond the maximum ceiling of 20 units in a regular semester constitutes an academic overload. Overload enrollment demands rigorous intellectual stamina and is restricted to students demonstrating outstanding scholarly competence.", body_style))
story.append(Paragraph("To qualify for an academic overload up to a hard ceiling of 23 credit units, a student must possess a cumulative grade point average (CGPA) of at least 3.50 on a 4.0 scale and must have successfully earned at least 30 credit units in residency at VinUniversity without any unexcused course failures or academic integrity infractions.", body_style))
story.append(Paragraph("Overload petitions must be initiated through the student academic portal no later than two weeks prior to the start of the semester and require written endorsement from the Academic Advisor, followed by formal sanction by the Program Director.", body_style))
story.append(Paragraph("First-year undergraduate students during their first two semesters of matriculation are categorically prohibited from undertaking academic course overload under any circumstances.", body_style))
story.append(PageBreak())

# Page 9
story.append(Paragraph("Section 2: Course Registration &amp; Credit Limits", heading1_style))
story.append(Paragraph("2.3 Add/Drop Course Period and Schedule Adjustment", heading2_style))
story.append(Paragraph("At the opening of each regular semester, an official Add/Drop Period is provided to enable students to modify their registered course schedules in response to curriculum requirements, instructor evaluations, and personal learning pace.", body_style))
story.append(Paragraph("The Add/Drop Period runs for exactly 14 calendar days (two full academic weeks) starting from 08:00 on the first day of class and ending at 17:00 on Friday of the second academic week. During this window, courses dropped do not appear on the student's permanent academic transcript, and no record of enrollment is retained.", body_style))
story.append(Paragraph("Adding courses is strictly subject to available seat capacity, meeting stated prerequisite requirements, and ensuring that no timetable scheduling conflicts exist with other enrolled courses. Faculty instructors do not possess authority to grant enrollment overrides beyond registered room fire-code safety capacities.", body_style))
story.append(Paragraph("Tuition charges are automatically reconciled based on the finalized credit total logged at the exact conclusion of the Add/Drop deadline.", body_style))
story.append(PageBreak())

# Page 10
story.append(Paragraph("Section 2: Course Registration &amp; Credit Limits", heading1_style))
story.append(Paragraph("2.4 Course Withdrawal Window and Prerequisites Enforcement", heading2_style))
story.append(Paragraph("Subsequent to the conclusion of the Add/Drop Period, a student may officially withdraw from an enrolled course between the beginning of the 3rd week and 17:00 on Friday of the 8th week of the regular semester.", body_style))
story.append(Paragraph("A course withdrawal results in a permanent recorded grade notation of 'W' on the student's official academic transcript. The 'W' grade carries no grade point weight and does not impact cumulative GPA calculation; however, tuition fees paid for withdrawn courses are entirely non-refundable.", body_style))
story.append(Paragraph("Students may not withdraw from a course if such withdrawal reduces their semester credit load below the mandatory 12-credit full-time minimum, unless granted medical leave by University Health Services. A student is permitted a maximum of three 'W' grades across their entire undergraduate tenure.", body_style))
story.append(Paragraph("All course prerequisites specified in the University Course Catalog are programmatically enforced by the Student Information System. Waivers for prerequisites require concurrent approval from the course instructor, Program Director, and College Curriculum Committee.", body_style))
story.append(PageBreak())

# ==========================================
# PAGES 11 - 14: SECTION 3 - ATTENDANCE & LEAVE
# ==========================================
# Page 11
story.append(Paragraph("Section 3: Class Attendance &amp; Leave of Absence", heading1_style))
story.append(Paragraph("3.1 Mandatory Attendance Standards and Classroom Engagement", heading2_style))
story.append(Paragraph("Active participation and regular physical classroom attendance are vital components of the participatory pedagogical philosophy at VinUniversity. Attendance is rigorously tracked across all lecture, seminar, discussion group, laboratory, and clinical sessions.", body_style))
story.append(Paragraph("Undergraduate students are required to maintain a minimum attendance rate of 80% of all scheduled instructional contact hours in each enrolled course. Failure to achieve 80% attendance without approved medical or university-sanctioned excused absence results in immediate academic disqualification from sitting the final course examination.", body_style))
story.append(Paragraph("Students disqualified for excessive absenteeism automatically receive a failing course grade of 'F' with 0.0 grade points, which is computed into both the semester and cumulative grade point averages. Instructors must issue formal written warnings to students whose cumulative unexcused absences exceed 10% of total contact hours.", body_style))
story.append(Paragraph("Tardiness exceeding 15 minutes past the scheduled class start time is recorded as a half-absence; three recorded tardies equal one full instructional absence in official attendance accounting.", body_style))
story.append(PageBreak())

# Page 12
story.append(Paragraph("Section 3: Class Attendance &amp; Leave of Absence", heading1_style))
story.append(Paragraph("3.2 Excused Absence Criteria and Documentation Protocol", heading2_style))
story.append(Paragraph("The university recognizes specific extenuating circumstances under which absences from instructional sessions may be designated as officially excused, preventing penalty against the 80% attendance threshold.", body_style))
story.append(Paragraph("Approved excused absences encompass documented acute medical illness or injury, significant bereavement involving immediate family members (parents, siblings, grandparents), mandatory legal obligations, and official participation in university-sanctioned athletic or academic competitions authorized by the Vice Provost of Academic Affairs.", body_style))
story.append(Paragraph("To obtain an excused absence, the student must submit an electronic Absence Request along with verifiable supporting documentation (such as hospital discharge certificates, medical certificates from Vinmec, or court summons) through the student portal within three business days of returning to campus.", body_style))
story.append(Paragraph("Even with verified excused absences, a student who misses more than 35% of total instructional contact hours in a course cannot receive a passing grade due to inadequate experiential exposure and must repeat the course in a subsequent term.", body_style))
story.append(PageBreak())

# Page 13
story.append(Paragraph("Section 3: Class Attendance &amp; Leave of Absence", heading1_style))
story.append(Paragraph("3.3 Voluntary Leave of Absence Application and Limits", heading2_style))
story.append(Paragraph("A student in good academic standing who faces personal, financial, family, or health challenges may submit a formal application for a Voluntary Leave of Absence (LOA) to temporarily pause their university studies without terminating degree candidacy.", body_style))
story.append(Paragraph("An approved Leave of Absence is granted for a duration of one or two consecutive regular semesters. The cumulative lifetime maximum allowance for voluntary leave of absence is two regular semesters across the entire undergraduate degree program.", body_style))
story.append(Paragraph("Applications for voluntary leave must be filed with the Office of the Registrar at least four weeks prior to the start of the prospective semester. Retroactive leave requests during an active semester are strictly prohibited except in cases of catastrophic medical emergency certified by a licensed medical board.", body_style))
story.append(Paragraph("During the period of an authorized Leave of Absence, the student retains their active university email account and library digital access but is ineligible to enroll in courses, reside in university dormitories, or utilize athletic campus facilities.", body_style))
story.append(PageBreak())

# Page 14
story.append(Paragraph("Section 3: Class Attendance &amp; Leave of Absence", heading1_style))
story.append(Paragraph("3.4 Re-enrollment After Leave and Administrative Withdrawal", heading2_style))
story.append(Paragraph("To resume active degree studies following an authorized Leave of Absence, the student must submit a formal Intent to Return Notice to the Registrar no later than 30 calendar days before the start of the intended semester.", body_style))
story.append(Paragraph("If the leave was granted for medical or psychological reasons, re-enrollment is strictly conditional upon submitting a comprehensive fit-for-study medical clearance evaluation signed by an accredited specialist physician and validated by the VinUniversity Health Center.", body_style))
story.append(Paragraph("Students who fail to submit the Intent to Return Notice or fail to register for courses by the end of the Add/Drop Period following the expiration of their approved leave are deemed to have abandoned their studies and will be subject to Administrative Withdrawal.", body_style))
story.append(Paragraph("An administratively withdrawn student seeking readmission must undergo the complete competitive admissions process de novo as a fresh applicant and cannot automatically reinstate previous scholarship commitments.", body_style))
story.append(PageBreak())

# ==========================================
# PAGES 15 - 18: SECTION 4 - GRADING & GPA
# ==========================================
# Page 15
story.append(Paragraph("Section 4: Grading System &amp; GPA Calculation", heading1_style))
story.append(Paragraph("4.1 Letter Grade Scale and Grade Point Equivalencies", heading2_style))
story.append(Paragraph("Academic performance in undergraduate courses at VinUniversity is evaluated using an alphabetical grading scale mapped to standard 4.0 numerical grade point equivalents. Instructors assign letter grades reflecting student mastery of stated course learning outcomes.", body_style))
story.append(Paragraph("The standard grading scale is structured as follows: Grade A+ (95-100%, 4.0 points, Exceptional); Grade A (90-94%, 4.0 points, Excellent); Grade A- (85-89%, 3.7 points, Very Good); Grade B+ (80-84%, 3.3 points, Good); Grade B (75-79%, 3.0 points, Satisfactory); Grade B- (70-74%, 2.7 points, Adequate).", body_style))
story.append(Paragraph("Lower passing performance is designated as: Grade C+ (65-69%, 2.3 points, Marginal Pass); Grade C (60-64%, 2.0 points, Minimum Major Pass); Grade D (50-59%, 1.0 point, Bare Pass, credit earned but cannot satisfy major core prerequisites). Grade F represents Failure (0-49%, 0.0 points, No credit earned).", body_style))
story.append(Paragraph("Special administrative notations include: P (Pass, credit earned, not calculated in GPA), NP (No Pass, zero credit), W (Withdrawn), and I (Incomplete).", body_style))
story.append(PageBreak())

# Page 16
story.append(Paragraph("Section 4: Grading System &amp; GPA Calculation", heading1_style))
story.append(Paragraph("4.2 Semester and Cumulative GPA Computation Formula", heading2_style))
story.append(Paragraph("The Semester Grade Point Average (SGPA) and Cumulative Grade Point Average (CGPA) serve as primary academic performance metrics determining academic standing, honor roll eligibility, and graduation readiness.", body_style))
story.append(Paragraph("SGPA is calculated by multiplying the grade point equivalent of the letter grade earned in each course by the credit units assigned to that course, summing these quality points across all courses taken during that term, and dividing by the total credit units attempted in that term. Quality point calculations are rounded to two decimal places.", body_style))
story.append(Paragraph("Courses evaluated on a Pass/No Pass (P/NP) basis, audit courses (AU), and withdrawn courses (W) are excluded entirely from both the numerator (quality points) and the denominator (attempted credit units).", body_style))
story.append(Paragraph("When an undergraduate student repeats a previously failed course (Grade F), both attempts remain visible on the official transcript, but only the higher grade earned is incorporated into the CGPA calculation, replacing the earlier failing grade point.", body_style))
story.append(PageBreak())

# Page 17
story.append(Paragraph("Section 4: Grading System &amp; GPA Calculation", heading1_style))
story.append(Paragraph("4.3 Incomplete Grade (I) Regulations and Conversion Timeline", heading2_style))
story.append(Paragraph("The notation 'I' (Incomplete) represents an interim designation granted solely when extraordinary, non-academic emergencies prevent a student from completing a minor remaining portion of course requirements (such as a final paper or exam) by term conclusion.", body_style))
story.append(Paragraph("To be eligible for an Incomplete grade, the student must have completed at least 70% of total course evaluation components with a cumulative passing average and must submit a formal Incomplete Contract co-signed by the course instructor prior to final examination week.", body_style))
story.append(Paragraph("All outstanding coursework specified in the Incomplete Contract must be finished and evaluated within four calendar weeks from the first day of instruction of the immediately subsequent regular semester.", body_style))
story.append(Paragraph("If the student fails to complete the required work within the mandatory four-week deadline, the recorded 'I' notation automatically and permanently converts to a default failing grade of 'F' on the student's academic record.", body_style))
story.append(PageBreak())

# Page 18
story.append(Paragraph("Section 4: Grading System &amp; GPA Calculation", heading1_style))
story.append(Paragraph("4.4 Grade Appeal Protocol and Independent Review Committee", heading2_style))
story.append(Paragraph("A student who has substantial reason to believe that a final recorded course grade was assigned arbitrarily, through mathematical miscalculation, or based on criteria disparate from the published course syllabus may initiate a formal Grade Appeal.", body_style))
story.append(Paragraph("The Grade Appeal process must be initiated within ten business days following official publication of final course grades on the university student portal. The student must first undertake an informal consultation with the course instructor to review grading rubrics and arithmetic accuracy.", body_style))
story.append(Paragraph("If informal consultation does not resolve the grievance, the student may file a formal written appeal accompanied by evidence to the College Grade Review Committee. A non-refundable processing fee of 500,000 VND is assessed, which is refunded in full if the appeal results in a positive grade adjustment.", body_style))
story.append(Paragraph("The decision rendered by the College Grade Review Committee following independent assessment by two external subject-matter faculty members is final and binding on all parties.", body_style))
story.append(PageBreak())

# ==========================================
# PAGES 19 - 22: SECTION 5 - ACADEMIC STANDING
# ==========================================
# Page 19
story.append(Paragraph("Section 5: Academic Standing, Warning &amp; Dismissal", heading1_style))
story.append(Paragraph("5.1 Categories of Academic Standing and Dean's List Criteria", heading2_style))
story.append(Paragraph("Academic standing is officially evaluated by the Registrar at the conclusion of each regular Fall and Spring semester. All enrolled undergraduate students are categorized under one of four statuses: Good Standing, Academic Warning, Academic Probation, or Academic Dismissal.", body_style))
story.append(Paragraph("To maintain Good Academic Standing, an undergraduate student must achieve both a Semester GPA (SGPA) and Cumulative GPA (CGPA) of at least 2.00 on a 4.0 scale.", body_style))
story.append(Paragraph("Students demonstrating superior academic excellence are honored with placement on the Dean's List. To qualify for the Dean's List in a given regular semester, an undergraduate must complete a minimum of 15 letter-graded credit units, attain an SGPA of 3.75 or higher, and have no recorded grade below 'B', no 'I' notations, and no academic integrity penalties.", body_style))
story.append(Paragraph("Dean's List honorees receive a formal certificate of commendation from the College Dean and notation on their permanent academic transcript.", body_style))
story.append(PageBreak())

# Page 20
story.append(Paragraph("Section 5: Academic Standing, Warning &amp; Dismissal", heading1_style))
story.append(Paragraph("5.2 Academic Warning Triggers and Mandatory Tutoring", heading2_style))
story.append(Paragraph("A student whose Semester GPA falls below 2.00 in any single semester, or whose Cumulative GPA falls between 1.80 and 1.99, is immediately placed on Academic Warning status for the subsequent semester.", body_style))
story.append(Paragraph("Academic Warning serves as an early institutional notification that the student is in jeopardy of academic failure. Students on Academic Warning are restricted to a maximum enrollment of 14 credit units during their warning semester to ensure dedicated focus on recovery.", body_style))
story.append(Paragraph("Students placed on Academic Warning are legally mandated to enter an Academic Improvement Contract with their designated Academic Advisor within the first week of classes. This contract includes compulsory weekly attendance in Peer Tutoring and Writing Center sessions.", body_style))
story.append(Paragraph("Failure to execute the Academic Improvement Contract or failure to attend mandatory tutoring sessions results in an administrative hold preventing registration for subsequent terms.", body_style))
story.append(PageBreak())

# Page 21
story.append(Paragraph("Section 5: Academic Standing, Warning &amp; Dismissal", heading1_style))
story.append(Paragraph("5.3 Academic Probation Criteria and Extracurricular Restrictions", heading2_style))
story.append(Paragraph("A student is placed on severe Academic Probation under either of two conditions: (1) failing to restore their Cumulative GPA to at least 2.00 after one semester on Academic Warning, or (2) earning a single semester GPA below 1.50 regardless of prior standing.", body_style))
story.append(Paragraph("Academic Probation is a critical intermediate status prior to institutional separation. A student on Academic Probation is restricted to enrolling in a maximum of 12 credit units and is required to retake all previously failed prerequisite courses offered in that term.", body_style))
story.append(Paragraph("During Academic Probation, the student is barred from participating in intercollegiate varsity athletics, holding elected leadership offices in student government or registered campus clubs, and participating in university-sponsored overseas study trips.", body_style))
story.append(Paragraph("Institutional scholarship funding is temporarily suspended while a student is on Academic Probation and may only be reinstated upon regaining Good Academic Standing.", body_style))
story.append(PageBreak())

# Page 22
story.append(Paragraph("Section 5: Academic Standing, Warning &amp; Dismissal", heading1_style))
story.append(Paragraph("5.4 Academic Dismissal Grounds and Appeal for Reinstatement", heading2_style))
story.append(Paragraph("An undergraduate student is subject to permanent Academic Dismissal from VinUniversity under the following explicit circumstances: (1) remaining on Academic Probation for two consecutive semesters without attaining a CGPA of 2.00, or (2) earning an SGPA below 1.00 in any individual semester.", body_style))
story.append(Paragraph("Notice of Academic Dismissal is communicated in writing by the Registrar following endorsement by the University Academic Standing Committee. Dismissed students are immediately unenrolled from all classes and required to vacate student housing within 48 hours.", body_style))
story.append(Paragraph("A dismissed student possesses the right to file a one-time Appeal for Academic Reinstatement to the Provost within seven business days of dismissal notification, based strictly on documented catastrophic life events that directly impaired academic execution.", body_style))
story.append(Paragraph("If reinstatement is granted by the Provost, the student returns under Final Probationary status with a non-negotiable target CGPA requirement of 2.20 to be achieved within one semester.", body_style))
story.append(PageBreak())

# ==========================================
# PAGES 23 - 26: SECTION 6 - ACADEMIC INTEGRITY
# ==========================================
# Page 23
story.append(Paragraph("Section 6: Academic Integrity &amp; Student Conduct", heading1_style))
story.append(Paragraph("6.1 Core Principles of Academic Honesty and Prohibited Conduct", heading2_style))
story.append(Paragraph("The intellectual life of VinUniversity is founded upon absolute honesty, intellectual transparency, and ethical responsibility in all dimensions of academic, clinical, and scientific endeavors. Any compromise of academic integrity undermines institutional credibility.", body_style))
story.append(Paragraph("Prohibited violations of academic honesty include: (a) Plagiarism, defined as incorporating the words, data, arguments, or intellectual schema of another author without appropriate citation; (b) Cheating, including unauthorized collaboration, copying answers during examinations, or utilizing prohibited crib sheets; (c) Fabrication of research, empirical data, or laboratory citations.", body_style))
story.append(Paragraph("Additional severe infractions encompass: (d) Bribery or attempted inducement of academic personnel; (e) Impersonation in assessments; and (f) Facilitating academic misconduct by distributing exam materials or commercializing academic assignments.", body_style))
story.append(Paragraph("Ignorance of citation guidelines or institutional regulations does not constitute a valid defense against charges of academic misconduct.", body_style))
story.append(PageBreak())

# Page 24
story.append(Paragraph("Section 6: Academic Integrity &amp; Student Conduct", heading1_style))
story.append(Paragraph("6.2 Responsible Use of Generative AI and Citation Rules", heading2_style))
story.append(Paragraph("VinUniversity recognizes generative artificial intelligence (GenAI) technologies as potentially transformative cognitive tools. However, their educational utilization must be strictly regulated to preserve authentic learning and student agency.", body_style))
story.append(Paragraph("The baseline institutional rule across all courses is that generative AI tools (such as ChatGPT, Claude, Copilot, or Gemini) may only be used when explicitly permitted in writing within the course syllabus or written assignment guidelines provided by the instructor.", body_style))
story.append(Paragraph("When AI utilization is permitted, students must provide explicit attribution in an 'AI Acknowledgement Section' detailing: the specific tool and model version employed, the complete prompt strings used, and a concise narrative explaining how generated outputs were verified, edited, and integrated.", body_style))
story.append(Paragraph("Submitting AI-generated prose, code, or data as one's original intellectual creation without explicit disclosure is classified as Category 2 Academic Misconduct, subject to mandatory punitive proceedings.", body_style))
story.append(PageBreak())

# Page 25
story.append(Paragraph("Section 6: Academic Integrity &amp; Student Conduct", heading1_style))
story.append(Paragraph("6.3 Classification of Violations and Sanction Framework", heading2_style))
story.append(Paragraph("Academic misconduct infractions are classified into three hierarchical severity tiers depending on intent, magnitude of impact, and prior disciplinary record.", body_style))
story.append(Paragraph("Category 1 (Minor Infractions): Unintentional minor citation errors, inadequate paraphrasing, or unauthorized peer collaboration on minor homework (worth under 10% of course grade). Sanctions: Written formal warning, mandatory completion of the Academic Integrity Tutorial, and maximum grade of zero on the specific assignment.", body_style))
story.append(Paragraph("Category 2 (Moderate Infractions): Substantial plagiarism in research papers, using unauthorized materials during quizzes, or unauthorized use of generative AI in midterms. Sanctions: Grade of 'F' for the course, formal disciplinary probation recorded in student file for two semesters.", body_style))
story.append(Paragraph("Category 3 (Severe/Repeat Infractions): Premeditated cheating on final exams, contract cheating, thesis fabrication, or repeat Category 2 offenses. Sanctions: Immediate suspension for 1-2 semesters or permanent expulsion with transcript notation.", body_style))
story.append(PageBreak())

# Page 26
story.append(Paragraph("Section 6: Academic Integrity &amp; Student Conduct", heading1_style))
story.append(Paragraph("6.4 Disciplinary Adjudication Procedures and Right to Appeal", heading2_style))
story.append(Paragraph("Allegations of academic misconduct are submitted to the University Academic Integrity Board (AIB). The student is notified in writing within five business days and is provided full access to all evidentiary materials.", body_style))
story.append(Paragraph("The AIB convenes a formal hearing where the student has the right to present oral testimony, submit corroborating documentary evidence, and be accompanied by a support advisor from the university community.", body_style))
story.append(Paragraph("The Board determines responsibility based on the preponderance of evidence (more likely than not). If found responsible, sanctions are determined according to Section 6.3 guidelines and communicated within three business days of hearing conclusion.", body_style))
story.append(Paragraph("Students may appeal the AIB decision to the University Provost within ten business days, strictly on grounds of procedural irregularity or the discovery of new compelling evidence previously unavailable during the original hearing.", body_style))
story.append(PageBreak())

# ==========================================
# PAGES 27 - 30: SECTION 7 - GRADUATION & HONORS
# ==========================================
# Page 27
story.append(Paragraph("Section 7: Degree Requirements, Graduation &amp; Honors", heading1_style))
story.append(Paragraph("7.1 Minimum Degree Completion Requirements and Residency", heading2_style))
story.append(Paragraph("To be awarded an undergraduate Bachelor's degree from VinUniversity, a candidate must successfully complete all prescribed curricular elements detailed in their program catalog within the allowable degree time horizon.", body_style))
story.append(Paragraph("The minimum requirement for bachelor's graduation is the completion of 128 academic semester credits for 4-year programs (such as Business Administration, Computer Science, and Data Science) and 150 credits for 5-year engineering programs. Students must achieve a minimum cumulative GPA (CGPA) of 2.00 on a 4.00 scale across all courses attempted.", body_style))
story.append(Paragraph("A strict Academic Residency Requirement mandates that at least 50% of the total credits required for the degree (minimum 64 credits), including all 3000-level and 4000-level major core courses, must be completed in direct residency at VinUniversity.", body_style))
story.append(Paragraph("Students must also satisfy non-credit mandatory graduation prerequisites: certification in National Defense and Security Education, completion of physical education modules, and documented completion of 100 hours of community service.", body_style))
story.append(PageBreak())

# Page 28
story.append(Paragraph("Section 7: Degree Requirements, Graduation &amp; Honors", heading1_style))
story.append(Paragraph("7.2 Degree Time Limits and Maximum Length of Study", heading2_style))
story.append(Paragraph("The expected normal duration of study for a standard undergraduate degree is four academic years (eight regular semesters) for standard Bachelor of Science and Bachelor of Arts curricula.", body_style))
story.append(Paragraph("The maximum allowable time limit to complete all degree requirements is six academic years (twelve regular semesters) for 4-year undergraduate programs, and seven academic years (fourteen regular semesters) for 5-year undergraduate engineering curricula.", body_style))
story.append(Paragraph("Approved leaves of absence do not count toward the maximum allowable duration of study, provided the total cumulative leave does not exceed the two-semester statutory limit set forth in Section 3.3.", body_style))
story.append(Paragraph("Any candidate who fails to fulfill all degree prerequisites within the prescribed maximum duration limit will have their degree candidacy automatically terminated without issuance of a diploma.", body_style))
story.append(PageBreak())

# Page 29
story.append(Paragraph("Section 7: Degree Requirements, Graduation &amp; Honors", heading1_style))
story.append(Paragraph("7.3 Graduation Clearance Protocol and Financial Audit", heading2_style))
story.append(Paragraph("During the final semester of anticipated enrollment, each degree candidate must file a formal Application for Graduation with the Office of the Registrar no later than the fourth week of the semester.", body_style))
story.append(Paragraph("Graduation clearance entails a multi-departmental institutional audit verifying: (1) academic audit of all general education, major core, and elective distribution credits; (2) library clearance confirming return of all borrowed media and settlement of overdue fines; (3) laboratory safety clearance; and (4) residential housing exit sign-off.", body_style))
story.append(Paragraph("Financial clearance from the University Finance Department verifying that all tuition fees, residential fees, library fines, and student health insurance liabilities have been settled in full is an absolute prerequisite for degree conferral.", body_style))
story.append(Paragraph("Diplomas and official academic transcripts will be withheld indefinitely until all outstanding financial liabilities to VinUniversity are liquidated in full.", body_style))
story.append(PageBreak())

# Page 30
story.append(Paragraph("Section 7: Degree Requirements, Graduation &amp; Honors", heading1_style))
story.append(Paragraph("7.4 Latin Honors and Valedictorian Selection Standards", heading2_style))
story.append(Paragraph("Undergraduate degree candidates graduating with exemplary academic distinction are recognized at Commencement with prestigious Latin Honors based strictly on final Cumulative GPA upon degree conferral.", body_style))
story.append(Paragraph("The criteria for Latin Honors are: Summa Cum Laude (With Highest Distinction) for graduates achieving a final CGPA of 3.90 to 4.00; Magna Cum Laude (With Great Distinction) for graduates achieving a final CGPA of 3.75 to 3.89; Cum Laude (With Distinction) for graduates achieving a final CGPA of 3.50 to 3.74.", body_style))
story.append(Paragraph("In addition to GPA benchmarks, eligibility for Latin Honors requires that the graduate has never been found responsible for any Category 2 or 3 violation of academic integrity and has completed at least 80% of degree credits in letter-graded coursework.", body_style))
story.append(Paragraph("The University Valedictorian is selected from among Summa Cum Laude graduates by a special faculty committee, factoring in scholarly research publications, leadership impact, and contribution to campus community life.", body_style))
story.append(PageBreak())

# ==========================================
# PAGES 31 - 35: SECTION 8 - TUITION & SCHOLARSHIPS
# ==========================================
# Page 31
story.append(Paragraph("Section 8: Tuition Schedule &amp; Scholarships", heading1_style))
story.append(Paragraph("8.1 Undergraduate Tuition Schedule and Payment Deadlines", heading2_style))
story.append(Paragraph("Tuition fees at VinUniversity are determined annually by the University Board of Trustees and reflect the high standards of faculty recruitment, research infrastructure, and experiential learning environments provided.", body_style))
story.append(Paragraph("For the 2025-2026 academic year, the published annual tuition fee for standard undergraduate programs in the College of Business Management and the College of Engineering &amp; Computer Science is 815,000,000 VND (equivalent to approximately 35,000 USD), billed in two equal semester installments.", body_style))
story.append(Paragraph("Tuition invoices are issued electronically 30 calendar days prior to the start of each semester. The mandatory payment deadline is 17:00 on the Friday preceding the first day of class for that semester. Late payments incur an automatic administrative late surcharge of 2% per month calculated on the unpaid balance.", body_style))
story.append(Paragraph("Students with outstanding unpaid tuition balances past the conclusion of the Add/Drop Period will have their course registrations cancelled and be placed on involuntary financial suspension.", body_style))
story.append(PageBreak())

# Page 32
story.append(Paragraph("Section 8: Tuition Schedule &amp; Scholarships", heading1_style))
story.append(Paragraph("8.2 Merit Scholarship Tiers and Award Amounts", heading2_style))
story.append(Paragraph("VinUniversity operates a merit scholarship program designed to attract and nurture outstanding academic talent regardless of socio-economic background. Merit scholarships are awarded upon admission and apply throughout standard degree duration.", body_style))
story.append(Paragraph("The institutional scholarship tiers comprise: (1) President's Scholarship: 100% full tuition waiver plus a living stipend of 35,000,000 VND per semester; (2) Dean's Scholarship: 90% tuition waiver; (3) Academic Merit Scholarship: 70% tuition waiver; and (4) University Talent Scholarship: 50% tuition waiver.", body_style))
story.append(Paragraph("All admitted undergraduate students receive an automatic baseline institutional subsidy of 35% tuition support funded by Vingroup, which is factored into tuition invoicing unless superseded by a higher merit scholarship tier.", body_style))
story.append(Paragraph("Scholarship awards apply directly against tuition fee invoices and cannot be disbursed as unallocated cash payments to recipient bank accounts.", body_style))
story.append(PageBreak())

# Page 33
story.append(Paragraph("Section 8: Tuition Schedule &amp; Scholarships", heading1_style))
story.append(Paragraph("8.3 Annual Scholarship Maintenance and CGPA Retention Thresholds", heading2_style))
story.append(Paragraph("Merit scholarship recipients must maintain rigorous academic and behavioral standards to sustain their financial scholarship awards across subsequent academic years. Scholarship status is formally reviewed annually at the conclusion of the Spring semester.", body_style))
story.append(Paragraph("To maintain scholarship eligibility, students must meet minimum cumulative GPA thresholds: Recipients of the 100% President's Scholarship and 90% Dean's Scholarship must maintain a Cumulative GPA (CGPA) of at least 3.50 on a 4.00 scale. Recipients of 70% and 50% scholarships must maintain a CGPA of at least 3.20.", body_style))
story.append(Paragraph("Furthermore, scholarship recipients must successfully earn at least 30 academic credit units across the combined Fall and Spring semesters of each academic year and must maintain Good Disciplinary Standing with zero recorded violations of the Student Code of Conduct.", body_style))
story.append(Paragraph("Failure to meet either the CGPA threshold or the credit completion requirement triggers automatic placement on Scholarship Probation for the following academic semester.", body_style))
story.append(PageBreak())

# Page 34
story.append(Paragraph("Section 8: Tuition Schedule &amp; Scholarships", heading1_style))
story.append(Paragraph("8.4 Scholarship Probation and Downgrade/Revocation Rules", heading2_style))
story.append(Paragraph("Scholarship Probation serves as an intervention grace period of one regular semester during which the student retains their current scholarship funding level while attempting to restore their CGPA to the prescribed benchmark.", body_style))
story.append(Paragraph("If, at the conclusion of the probationary semester, the student fails to restore their CGPA to the required threshold, the scholarship is subjected to a tiered downgrade: A 100% or 90% scholarship is downgraded to a 50% award; a 70% or 50% scholarship is completely revoked, reverting the student to standard tuition liability.", body_style))
story.append(Paragraph("A student who is found responsible for any Category 2 or Category 3 violation of academic integrity or serious student conduct infraction suffers immediate, permanent, and irrevocable revocation of all university scholarship awards without probation.", body_style))
story.append(Paragraph("Scholarship revocations take effect immediately for the next billing cycle and cannot be appealed except in proven cases of grade recording miscalculation.", body_style))
story.append(PageBreak())

# Page 35
story.append(Paragraph("Section 8: Tuition Schedule &amp; Scholarships", heading1_style))
story.append(Paragraph("8.5 Need-Based Financial Aid and Tuition Refund Schedule", heading2_style))
story.append(Paragraph("Students with demonstrable financial hardship may apply for Need-Based Financial Aid to supplement merit scholarships. Financial aid applications require certified tax returns, household income documentation, and bank statements submitted annually to the Financial Aid Office.", body_style))
story.append(Paragraph("Need-based aid awards range from 20% to 80% of remaining tuition liability and may include on-campus student work-study stipends providing up to 20 hours per week of paid administrative or research assistantship employment.", body_style))
story.append(Paragraph("For students who officially withdraw from the university during an active semester, tuition fee refunds are strictly prorated according to the following schedule: (1) Withdrawal during Week 1-2 (Add/Drop Period): 100% tuition refund less non-refundable deposit; (2) Withdrawal during Week 3-4: 50% tuition refund; (3) Withdrawal during Week 5-6: 25% tuition refund; (4) Withdrawal after Week 6: 0% refund (no refund).", body_style))
story.append(Paragraph("Residential dormitory fees and university dining plan charges are non-refundable after the conclusion of the second week of the semester.", body_style))
story.append(PageBreak())

# ==========================================
# PAGE 36: APPENDIX & REGULATORY TERMS (Excluded from content)
# ==========================================
story.append(Paragraph("APPENDIX: Glossary of Regulatory Terms &amp; Authorities", heading1_style))
story.append(Paragraph("This handbook is promulgated under the authority of the University Provost and Academic Council of VinUniversity. References to statutory regulations correspond to Law on Higher Education No. 34/2018/QH14 of the Socialist Republic of Vietnam.", body_style))
story.append(Paragraph("Key Governing Bodies: University Academic Integrity Board (AIB), College Grade Review Committee (CGRC), Office of the University Registrar, Student Affairs Office, and Student Financial Aid Committee.", body_style))
story.append(Paragraph("For administrative inquiries regarding course registration, transcripts, and degree verification, contact registrar@vinuni.edu.vn. For scholarship maintenance questions, contact scholarship@vinuni.edu.vn.", body_style))
story.append(Paragraph("All policies herein are subject to periodic review and amendment by the Academic Council. Amendments take effect upon official publication on the institutional website.", body_style))

doc.build(story)
print(f"Generated PDF: {pdf_path}")
