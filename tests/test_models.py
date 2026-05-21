from pydantic import ValidationError

from prismaflow import PrismaFlow, PrismaTemplate


def make_flow() -> PrismaFlow:
    return PrismaFlow.new_review(
        title="Example",
        records_identified_databases=1240,
        records_identified_registers=50,
        records_removed_duplicates=210,
        records_removed_automation=0,
        records_removed_other=0,
        records_screened=1080,
        records_excluded=950,
        reports_sought=130,
        reports_not_retrieved=10,
        reports_assessed=120,
        reports_excluded={"Wrong population": 30, "Wrong intervention": 20},
        studies_included=70,
    )


def test_new_review_builds_model() -> None:
    flow = make_flow()
    assert flow.template is PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS
    assert flow.identification.records_identified_total == 1290
    assert flow.screening.records_removed_total == 210
    assert flow.eligibility.reports_excluded_total == 50


def test_negative_count_is_rejected() -> None:
    kwargs = make_flow().model_dump()
    kwargs["included"]["studies_included"] = -1
    try:
        PrismaFlow.model_validate(kwargs)
    except ValidationError as exc:
        assert "studies_included" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("negative counts should fail validation")
