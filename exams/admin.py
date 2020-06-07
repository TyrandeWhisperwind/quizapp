from django.contrib import admin
import nested_admin
from .models import Exam, Questions, Options, Candidate,CandidateResponse,TakenExam

class OptionsInline(nested_admin.NestedTabularInline):
 model = Options
 extra = 4



class QuestionsInline(nested_admin.NestedTabularInline):
 model = Questions
 inlines = [OptionsInline,]
 extra = 1


#nested_admin.NestedModelAdmin is a special model in admin
class ExamAdmin(nested_admin.NestedModelAdmin):
 inlines = [QuestionsInline,]


class CandidateResponseInline(admin.TabularInline):
 model = CandidateResponse


class CandidateAdmin(admin.ModelAdmin):
 model = Candidate



admin.site.register(Exam, ExamAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateResponse)
admin.site.register(TakenExam)
