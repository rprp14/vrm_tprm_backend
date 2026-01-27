@action(detail=True, methods=["post"])
def approve(self, request, pk=None):
    review = self.get_object()

    validate_transition(
        entity="assessment",
        action="approve",
        from_status=review.assessment.status,
        role=request.user.role,
        context={
            "no_open_remediation": True
        }
    )

    review.assessment.status = "Approved"
    review.assessment.save()
    return Response({"message": "Assessment approved"})
