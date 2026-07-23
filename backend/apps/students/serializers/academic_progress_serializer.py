from rest_framework import serializers


class AcademicIdentitySerializer(serializers.Serializer):
    university = serializers.CharField()
    program = serializers.CharField()
    current_semester = serializers.IntegerField()
    joined_session = serializers.CharField()
    academic_status = serializers.CharField()
    expected_graduation_date = serializers.DateField()


class CurrentCourseSerializer(serializers.Serializer):
    course_code = serializers.CharField(source="program_course.course_code")
    course_title = serializers.CharField(source="program_course.course.title")
    credit_hours = serializers.IntegerField(source="program_course.total_credit_hours")
    status = serializers.CharField()


class CurrentSemesterSerializer(serializers.Serializer):
    current_courses = CurrentCourseSerializer(many=True)
    current_credit_hours = serializers.IntegerField()
    semester_gpa = serializers.DecimalField(max_digits=4, decimal_places=2)


class DegreeProgressSerializer(serializers.Serializer):
    completed_credit_hours = serializers.IntegerField()
    remaining_credit_hours = serializers.IntegerField()
    completed_courses = serializers.IntegerField()
    remaining_courses = serializers.IntegerField()
    total_program_credit_hours = serializers.IntegerField()
    total_program_courses = serializers.IntegerField()
    progress_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class AcademicPerformanceSerializer(serializers.Serializer):
    cgpa = serializers.DecimalField(max_digits=4, decimal_places=2)


class AssignmentSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    course_name = serializers.CharField()
    title = serializers.CharField()
    due_date = serializers.DateField()
    status = serializers.CharField()


class AssignmentsDueSoonSerializer(serializers.Serializer):
    upcoming = AssignmentSummarySerializer(many=True)
    overdue = AssignmentSummarySerializer(many=True)


class TimetableTodayEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    course_name = serializers.CharField()
    day_of_week_display = serializers.CharField(source="get_day_of_week_display")
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    location = serializers.CharField()


class RecentNoteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    course_title = serializers.CharField(source="course.title")
    main_heading = serializers.CharField()
    sub_heading = serializers.CharField()
    uploaded_by = serializers.CharField(source="uploader.get_full_name")
    created_at = serializers.DateTimeField()


class FlashcardsSummarySerializer(serializers.Serializer):
    available_decks = serializers.IntegerField()
    cards_reviewed = serializers.IntegerField()
    cards_known = serializers.IntegerField()


class MyQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    course_title = serializers.CharField(source="course.title")
    title = serializers.CharField()
    answer_count = serializers.IntegerField()
    is_resolved = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class MyAnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_title = serializers.CharField(source="question.title")
    body = serializers.CharField()
    is_accepted = serializers.BooleanField()
    vote_count = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class QAActivitySerializer(serializers.Serializer):
    my_questions = MyQuestionSerializer(many=True)
    my_answers = MyAnswerSerializer(many=True)


class CourseAttendanceSerializer(serializers.Serializer):
    course_code = serializers.CharField()
    course_title = serializers.CharField()
    total_sessions = serializers.IntegerField()
    present_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    leave_count = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()


class AttendanceOverviewSerializer(serializers.Serializer):
    overall_percentage = serializers.FloatField()
    courses = CourseAttendanceSerializer(many=True)
    at_risk_courses = serializers.ListField(child=serializers.CharField())


class AcademicProgressDashboardSerializer(serializers.Serializer):
    academic_identity = AcademicIdentitySerializer()
    current_semester = CurrentSemesterSerializer()
    degree_progress = DegreeProgressSerializer()
    performance = AcademicPerformanceSerializer()
    assignments_due_soon = AssignmentsDueSoonSerializer()
    timetable_today = TimetableTodayEntrySerializer(many=True)
    recent_notes = RecentNoteSerializer(many=True)
    flashcards = FlashcardsSummarySerializer()
    qa_activity = QAActivitySerializer()
    attendance = AttendanceOverviewSerializer()