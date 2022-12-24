from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentGradeSchema,AssignmentSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    teacher_assignments = Assignment.get_assignments_teacher(p.teacher_id)
    teacher_assignment_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignment_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    assignment = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.grade_assignment(assignment, p)
    db.session.commit() 
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

    return APIResponse.respond(data=graded_assignment_dump)
