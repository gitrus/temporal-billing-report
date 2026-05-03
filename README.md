# temporal-billing-report

Temporal workflow that fetches invoice data and generates a billing report.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [uv](https://docs.astral.sh/uv/)

## Setup

```sh
make install
```

## Running

Start Temporal (server + UI):

```sh
make up
```

In a separate terminal, start the worker:

```sh
make worker
```

Trigger a workflow run:

```sh
make run
```

Temporal UI is available at http://localhost:8080.

## Stop

```sh
make down
```

## Structure

```
src/
  domain/
    models.py              # Pydantic request/response models
    workflow/workflow.py   # BillingReportWorkflow
  temporal/
    names.py               # WorkflowName / ActivityName enums
    worker.py              # worker setup
  transport/
    activities/
      activities.py        # fetch_invoice_data, generate_report
cmd/
  worker.py                # entry point
hello.py                   # workflow starter (dev)
```
