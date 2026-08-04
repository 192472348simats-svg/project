import random
from typing import Dict, Any, List, Optional
from .analytics import StudentAnalytics


class ParagraphBuilder:
    """
    Paragraph Builder Engine: Assembles professional, multi-paragraph parent letters
    from modular, rotating sentence banks. Replicates the exact writing style of NEW.pptx
    while ensuring every student's report is slightly varied and non-repetitive.
    """

    # 1. Introduction Bank (Addresses Parents & References Academic Progress)
    INTRO_BANK = [
        "Dear Parents, The previous slide contains a detailed summary of your {ward_term}'s academic progress, including the subjects {pronoun_he} has successfully completed, the number of pending arrears (if any), the courses {pronoun_he} is currently pursuing, and {pronoun_his} attendance percentage in each subject. We kindly request you to spend a few minutes reviewing these details carefully. A constructive discussion with your {ward_child} regarding {pronoun_his} academic strengths, areas that require improvement, and future learning goals will greatly motivate {pronoun_him} to perform better. Your continuous encouragement, guidance, and timely support play a vital role in shaping {pronoun_his} academic journey and preparing {pronoun_him} for future opportunities.",

        "Dear Parents, The academic information related to your {ward_child} has already been presented in the previous slide for your reference. It includes the list of courses {pronoun_he} has completed, details of any existing arrears, the subjects {pronoun_he} is presently studying, and {pronoun_his} attendance percentage in each course. We sincerely request you to review this information thoroughly and discuss {pronoun_his} academic performance with {pronoun_him}. Such conversations at home often inspire students to become more responsible, disciplined, and focused on achieving better academic outcomes. Your valuable encouragement and consistent monitoring will greatly contribute to {pronoun_his} educational growth and future success.",

        "Dear Parents, A comprehensive overview of your {ward_term}'s academic record has already been shared in the previous slide. The information includes the courses {pronoun_he} has completed successfully, any arrears that are yet to be cleared, the courses {pronoun_he} is currently attending, and the corresponding attendance percentage. We request you to carefully review these details and have a meaningful discussion with your {ward_child} regarding {pronoun_his} academic progress. Your guidance and motivation will help {pronoun_him} recognize the importance of consistent effort, regular attendance, and dedicated preparation, thereby enabling {pronoun_him} to achieve better academic performance in the coming semesters.",

        "Dear Parents, The previous slide provides complete information regarding your {ward_term}'s academic performance, including the subjects {pronoun_he} has already completed, {pronoun_his} arrear status, the courses in which {pronoun_he} is currently enrolled, and the attendance percentage for each subject. We request you to examine these details carefully and discuss them with {pronoun_him} at home. Your positive guidance and encouragement will help {pronoun_him} remain committed to {pronoun_his} studies, improve {pronoun_his} academic performance, and prepare {pronoun_himself} effectively for future career opportunities. Continuous parental involvement plays an important role in a student's educational success.",

        "Dear Parents, We have already shared your {ward_term}'s academic profile in the previous slide, which contains details of the courses {pronoun_he} has completed, any pending arrears, the subjects {pronoun_he} is presently pursuing, and {pronoun_his} attendance percentage. We sincerely request you to review this information with care and have an encouraging conversation with your {ward_child} about {pronoun_his} academic responsibilities and future goals. Your support, appreciation, and timely guidance will inspire {pronoun_him} to remain focused, improve {pronoun_his} academic performance, and work consistently towards achieving greater success throughout {pronoun_his} educational journey.",

        "Dear Parents, A detailed summary of your {ward_term}'s academic performance has already been presented in the previous slide for your reference. The report contains information regarding the courses {pronoun_he} has completed, any pending arrears, the subjects {pronoun_he} is currently studying, and {pronoun_his} attendance percentage. We kindly request you to go through these details thoroughly and have a constructive conversation with your {ward_child} regarding {pronoun_his} academic progress. Your encouragement, appreciation, and regular guidance will inspire {pronoun_her_him} to stay committed to {pronoun_his} studies and continue working towards academic excellence.",

        "Dear Parents, The academic record of your {ward_child} has already been displayed in the previous slide for your kind reference. It includes the list of courses {pronoun_he} has successfully completed, details of any pending arrears, the subjects {pronoun_he} is currently studying, and {pronoun_his} attendance percentage in each course. We sincerely request you to review these details carefully and discuss {pronoun_his} academic progress with {pronoun_him}. Your valuable guidance, encouragement, and regular interaction regarding {pronoun_his} studies will help {pronoun_him} understand the importance of maintaining consistent academic performance.",

        "Dear Parents, A summary of your {ward_term}'s academic performance has already been provided in the previous slide. The information includes the courses {pronoun_he} has completed, {pronoun_his} current arrear status, the subjects in which {pronoun_he} is presently enrolled, and {pronoun_his} attendance percentage for each course. We kindly request you to go through these academic details carefully and have a positive discussion with your {ward_child} regarding {pronoun_his} progress.",

        "Dear Parents, The academic details of your {ward_child} have already been shared in the previous slide for your valuable reference. The information includes the courses {pronoun_he} has successfully completed, the status of any pending arrears, the courses {pronoun_he} is currently pursuing, and {pronoun_his} attendance percentage. We request you to review these details carefully and spend some time discussing {pronoun_his} academic progress with {pronoun_him}.",

        "Dear Parents, Kindly refer to the previous slide, where your {ward_term}'s academic information has been presented in detail. It contains the list of subjects {pronoun_he} has completed successfully, information regarding any pending arrears, the courses {pronoun_he} is currently pursuing, and {pronoun_his} attendance percentage. We request you to carefully review these details and have a meaningful conversation with {pronoun_him} about {pronoun_his} academic responsibilities and future goals."
    ]

    # 2. Recent Events Bank
    EVENTS_BANK = [
        "We are pleased to inform you that our institution successfully celebrated {recent_events}, the College Cultural Festival, providing students with an excellent platform to exhibit their creativity, talents, leadership qualities, and team spirit beyond the academic curriculum.",
        "It gives us immense pleasure to share that our institution celebrated {recent_events}, the annual College Cultural Festival, where students enthusiastically showcased their talents, creativity, leadership abilities, and collaborative skills.",
        "We are happy to announce that {recent_events}, our College Cultural Festival, was celebrated with great enthusiasm, offering students a valuable opportunity to demonstrate their artistic talents, innovation, leadership, and teamwork.",
        "We are delighted to share that our institution proudly organized {recent_events}, the College Cultural Festival, enabling students to express their creativity and strengthen their leadership and teamwork skills beyond academics.",
        "We are glad to inform you that our college successfully conducted {recent_events}, a vibrant cultural celebration that encouraged students to display their hidden talents, creativity, leadership, and collaborative abilities.",
        "Our institution was delighted to celebrate {recent_events}, the annual College Cultural Festival, where students actively participated and showcased their creativity, talents, leadership potential, and team spirit.",
        "We are pleased to share that {recent_events} was celebrated with great excitement, providing students with a meaningful platform to demonstrate their abilities in creativity, leadership, teamwork, and cultural excellence.",
        "Our institution recently celebrated {recent_events}, the College Cultural Festival, providing students with a vibrant platform to express their creativity and enhance their leadership and teamwork abilities.",
        "We are proud to inform you that our institution celebrated {recent_events}, creating an inspiring environment for students to explore their creativity, develop leadership skills, and strengthen teamwork.",
        "We are delighted to announce the successful celebration of {recent_events}, where students enthusiastically participated and showcased their talents, innovation, leadership, and collaborative skills."
    ]

    # 3. NPTEL Headers
    NPTEL_HEADER_BANK = [
        "Regarding {pronoun_his} NPTEL enrolment, {pronoun_he} has registered for the following courses:",
        "His NPTEL course registration details are as follows:" if True else "Her NPTEL course registration details are as follows:",
        "The details of {pronoun_his} NPTEL registrations are given below:",
        "{pronoun_his_cap} NPTEL course registration details are listed below:",
        "{pronoun_his_cap} NPTEL enrolment details are as follows:"
    ]

    # 4. Code of Conduct / Discipline Bank
    DISCIPLINE_BANK = [
        "We also request your support in reminding {pronoun_him} to strictly follow the institutional code of conduct. {pronoun_he_cap} should wear {pronoun_his} official SIMATS Identity Card at all times while inside the campus. {pronoun_his_cap} hair should be neatly maintained, and {pronoun_he} should either remain clean-shaven or keep {pronoun_his} beard properly trimmed. {pronoun_he_cap} is expected to attend classes in clean, neatly pressed, and respectable attire along with appropriate shoes.",

        "Kindly ensure that {pronoun_he} follows the general guidelines prescribed by the institution. {pronoun_he_cap} must wear {pronoun_his} SIMATS ID card throughout {pronoun_his} stay on campus. {pronoun_his_cap} hairstyle should be neat and presentable, while {pronoun_his} beard should either be cleanly shaved or maintained in a tidy manner. Students are expected to report to the campus wearing clean, properly ironed, and decent clothing along with shoes.",

        "We also seek your cooperation in ensuring that {pronoun_he} follows all institutional regulations. Wearing the official SIMATS ID card inside the campus is mandatory. {pronoun_his_cap} hair should be properly groomed, and if {pronoun_he} keeps a beard, it should be neatly trimmed; otherwise, {pronoun_he} should remain clean-shaven. Students should attend classes wearing clean, ironed, and modest attire along with appropriate footwear.",

        "We kindly request you to reinforce the importance of following the institution's discipline guidelines. Your {ward_child} should wear {pronoun_his} SIMATS identity card throughout {pronoun_his} time on campus. {pronoun_his_cap} hairstyle must be neat, and {pronoun_his} beard should either be properly trimmed or completely shaved. Students are expected to wear clean, well-maintained, and decent clothing along with shoes every day.",

        "We also request your cooperation in helping {pronoun_him} follow the institution's general rules and regulations. {pronoun_he_cap} should always display {pronoun_his} official SIMATS ID card while inside the campus premises. {pronoun_his_cap} hair should be neatly maintained, and {pronoun_his} beard should either be clean-shaven or properly trimmed. Students are expected to attend the institution in neat, clean, and well-ironed attire with appropriate footwear.",

        "We also request your support in ensuring that {pronoun_she_he} follows the institution's general rules and regulations. {pronoun_she_he_cap} should wear {pronoun_her_his} official SIMATS Identity Card at all times while inside the campus. {pronoun_she_he_cap} is expected to maintain a neat and professional appearance and attend the institution in clean, properly ironed, and decent attire along with appropriate footwear.",

        "We also request your cooperation in ensuring that {pronoun_he} follows the institution's discipline and dress code. {pronoun_he_cap} should always wear {pronoun_his} official SIMATS Identity Card while inside the campus. {pronoun_his_cap} hairstyle must be neat and properly maintained. If {pronoun_he} keeps a beard, it should be neatly trimmed; otherwise, {pronoun_he} should remain clean-shaven.",

        "Kindly encourage {pronoun_her_him} to follow all institutional guidelines with sincerity. {pronoun_she_he_cap} should always wear {pronoun_her_his} official SIMATS Identity Card while on campus. Students are expected to maintain a neat and decent appearance by wearing clean, properly maintained, and well-ironed attire along with suitable shoes.",

        "We kindly request your cooperation in reminding {pronoun_her_him} to follow the institution's regulations. {pronoun_she_he_cap} should wear {pronoun_her_his} official SIMATS Identity Card throughout {pronoun_her_his} stay on campus. Students are expected to maintain a neat appearance and attend classes in clean, well-maintained, and respectable attire along with proper footwear.",

        "We seek your valuable support in ensuring that {pronoun_he} follows all institutional guidelines. {pronoun_he_cap} should wear {pronoun_his} official SIMATS Identity Card at all times while on campus. {pronoun_his_cap} hair must be neatly cut and properly groomed. {pronoun_his_cap} beard should either be completely shaved or neatly trimmed according to the institution's standards."
    ]

    # 5. Technical Activities Bank
    TECH_ACTIVITIES_BANK = [
        "In addition to regular academics, we strongly encourage {pronoun_him} to participate actively in technical events such as hackathons, seminars, workshops, coding competitions, and code debugging activities, which will significantly enhance {pronoun_his} technical knowledge, confidence, and career readiness.",
        "We also encourage {pronoun_him} to make effective use of the opportunities provided by participating in hackathons, seminars, technical workshops, programming contests, and code debugging sessions to improve {pronoun_his} practical skills and overall professional development.",
        "Beyond classroom learning, we strongly encourage {pronoun_him} to participate in technical programs such as seminars, hackathons, code debugging events, workshops, and similar activities that will strengthen {pronoun_his} technical competence, communication skills, teamwork, and confidence.",
        "Additionally, encourage {pronoun_him} to take part in technical events including hackathons, seminars, code debugging competitions, workshops, and other skill-development activities that will broaden {pronoun_his} knowledge, improve problem-solving abilities, and prepare {pronoun_him} for industry expectations.",
        "Furthermore, we encourage {pronoun_him} to actively participate in various technical activities such as hackathons, seminars, coding events, workshops, and code debugging competitions. These opportunities will help {pronoun_him} enhance {pronoun_his} technical expertise, improve analytical thinking, and develop confidence.",
        "We further encourage {pronoun_her_him} to actively participate in technical programmes such as hackathons, seminars, workshops, coding competitions, and code debugging sessions. Such participation will enhance {pronoun_her_his} technical knowledge, analytical thinking, communication skills, and overall career readiness.",
        "We further encourage {pronoun_him} to participate actively in technical activities such as hackathons, seminars, workshops, coding competitions, and code debugging sessions to strengthen {pronoun_his} technical knowledge and overall professional development.",
        "We also recommend that {pronoun_she_he} actively participate in various technical activities including hackathons, seminars, technical workshops, coding events, and code debugging competitions. These opportunities will help {pronoun_her_him} strengthen {pronoun_her_his} practical knowledge and problem-solving abilities.",
        "We also encourage {pronoun_her_him} to make the best use of technical learning opportunities by participating in hackathons, seminars, workshops, programming contests, and code debugging sessions to prepare for future professional success.",
        "We also encourage {pronoun_him} to participate enthusiastically in technical programmes such as hackathons, seminars, workshops, code debugging competitions, and similar activities."
    ]

    @classmethod
    def generate_parent_letter(
        cls,
        analytics: StudentAnalytics,
        recent_events: str = "SIMMAM 2026",
        mentor_name: str = "Dr. T. Kumaragurubaran",
        mentor_phone: str = "7373032383",
        seed: Optional[int] = None
    ) -> str:
        """
        Assembles the complete parent letter for Slide 2 matching NEW.pptx formatting.
        Uses deterministic hashing based on student Reg No to select rotating phrases.
        """
        reg_no = analytics.reg_no
        reg_hash = hash(reg_no + (str(seed) if seed else "")) % 1000

        # Gender pronoun detection (default male unless name/dept indicates female)
        is_female = cls._is_female(analytics.name)
        
        ward_term = "daughter" if is_female else "son"
        ward_child = "daughter" if is_female else "son"
        pronoun_he = "she" if is_female else "he"
        pronoun_he_cap = "She" if is_female else "He"
        pronoun_his = "her" if is_female else "his"
        pronoun_his_cap = "Her" if is_female else "His"
        pronoun_him = "her" if is_female else "him"
        pronoun_she_he = "she" if is_female else "he"
        pronoun_she_he_cap = "She" if is_female else "He"
        pronoun_her_his = "her" if is_female else "his"
        pronoun_her_him = "her" if is_female else "him"
        pronoun_himself = "herself" if is_female else "himself"

        kw = {
            "ward_term": ward_term,
            "ward_child": ward_child,
            "pronoun_he": pronoun_he,
            "pronoun_he_cap": pronoun_he_cap,
            "pronoun_his": pronoun_his,
            "pronoun_his_cap": pronoun_his_cap,
            "pronoun_him": pronoun_him,
            "pronoun_himself": pronoun_himself,
            "pronoun_she_he": pronoun_she_he,
            "pronoun_she_he_cap": pronoun_she_he_cap,
            "pronoun_her_his": pronoun_her_his,
            "pronoun_her_him": pronoun_her_him,
            "recent_events": recent_events or "SIMMAM 2026"
        }

        # 1. Select Paragraph 1 (Intro)
        p1_idx = reg_hash % len(cls.INTRO_BANK)
        p1 = cls.INTRO_BANK[p1_idx].format(**kw)

        # 2. Select Paragraph 2 (Recent Events)
        p2_idx = (reg_hash + 1) % len(cls.EVENTS_BANK)
        p2 = cls.EVENTS_BANK[p2_idx].format(**kw)

        # 3. Format NPTEL Paragraph
        nptel_courses_raw = analytics.nptel_courses
        if not nptel_courses_raw or nptel_courses_raw.strip().lower() in ["none", "nil", "n/a", "not registered"]:
            p3 = f"Regarding {kw['pronoun_his']} NPTEL enrolment, {kw['pronoun_he']} has not registered for courses yet. After so many instructions, we request your support in this regard and motivate your ward to register the course ASAP."
        else:
            header_idx = (reg_hash + 2) % len(cls.NPTEL_HEADER_BANK)
            nptel_header = cls.NPTEL_HEADER_BANK[header_idx].format(**kw)
            
            # Format bullet points
            nptel_list = [c.strip() for c in nptel_courses_raw.split(",") if c.strip()]
            bullets = []
            for course in nptel_list:
                if "-" in course:
                    bullets.append(f"•  {course}")
                else:
                    bullets.append(f"•  {course} – The course is scheduled to commence on 20 July.")
            p3 = nptel_header + "\n" + "\n".join(bullets)

        # 4. Select Paragraph 4 (Discipline & Grooming)
        p4_idx = (reg_hash + 3) % len(cls.DISCIPLINE_BANK)
        p4 = cls.DISCIPLINE_BANK[p4_idx].format(**kw)

        # 5. Select Paragraph 5 (Tech Activities & Sign-off)
        p5_idx = (reg_hash + 4) % len(cls.TECH_ACTIVITIES_BANK)
        tech_text = cls.TECH_ACTIVITIES_BANK[p5_idx].format(**kw)
        
        signoff = f" With Regards, {mentor_name}, {mentor_phone}."
        p5 = p4 + " " + tech_text + signoff

        # Combine paragraphs cleanly
        full_letter = f"{p1}\n{p2}\n{p3}\n{p5}"
        return full_letter

    @staticmethod
    def _is_female(name: str) -> bool:
        """
        Simple heuristic for gender pronouns.
        """
        female_names = [
            "latisha", "divya", "haripriya", "rahima", "sree", "samyuktha",
            "prethepa", "yogashree", "bhavana", "pooja", "priya", "kavitha", "anitha"
        ]
        name_lower = name.lower()
        return any(fn in name_lower for fn in female_names)
