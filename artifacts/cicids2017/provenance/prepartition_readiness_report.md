# PRE-PARTITION Readiness — CICIDS2017

- **Master SHA-256:** `b68a108f6fe44082a051e2ab81a4bd8859cb3ccd417ff60623871155d51cabd3`
- **Global protocol hash:** `55713fd82c01168e0a906d282644b1c8dff88632dcb82512c5f62c637e35ff1f`
- **Taxonomy hash:** `e4290a4c91d69236e84f294fdadde7eda7f94aaa7dd6c319ade3405c75a1513a`
- **Row identity specification hash:** `75d07ee359615a65b65107ba4999df581e382e13395916865b96a34e3faf5624`
- **Raw feature-policy hash:** `3cae0d0bb613b1966f2542c2211afadcf4cdc2bcb6ceb9017ad51703c1b9dc32`
- **Blocking failures:** 0
- **Warnings:** 4
- **PRE-PARTITION READINESS:** **PASS_WITH_NONBLOCKING_WARNINGS**
- **Next authorized stage:** Sections 8–11: group-aware partition design and immutable partition construction

## Section status

| section | status |
| --- | --- |
| 1 | PASS |
| 2 | PASS |
| 3 | PASS |
| 4 | PASS |
| 5 | PASS |
| 6 | PASS |
| 7 | PASS |

## Blocking failures
- None

## Nonblocking warnings
- Section 3: Duplicate names exist in the serialized raw header. They remain distinct only through parser-visible positional disambiguation and are explicitly recorded: [' Fwd Header Length']
- Section 3: Parser-visible names consistent with duplicate-header mangling: [' Fwd Header Length.1']
- Section 7: 94,781 same-label model-view duplicate groups were observed and retained as future indivisible allocation groups.
- Section 7: 698 mixed-label/conflicting model-view groups were observed and retained; they are ineligible for benign-only future partitions.
