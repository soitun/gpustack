from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from gpustack.api.exceptions import (
    AlreadyExistsException,
    InternalServerErrorException,
    NotFoundException,
)
from gpustack.server.deps import ListParamsDep, SessionDep, EngineDep
from gpustack.schemas.workers import (
    WorkerCreate,
    WorkerPublic,
    WorkerUpdate,
    WorkersPublic,
    Worker,
)
from gpustack.server.services import WorkerService

router = APIRouter()


@router.get("", response_model=WorkersPublic)
async def get_workers(
    engine: EngineDep,
    session: SessionDep,
    params: ListParamsDep,
    name: str = None,
    search: str = None,
    uuid: str = None,
):
    fuzzy_fields = {}
    if search:
        fuzzy_fields = {"name": search}

    fields = {}
    if name:
        fields = {"name": name}
    if uuid:
        fields["worker_uuid"] = uuid

    if params.watch:
        return StreamingResponse(
            Worker.streaming(engine, fields=fields, fuzzy_fields=fuzzy_fields),
            media_type="text/event-stream",
        )

    return await Worker.paginated_by_query(
        session=session,
        fields=fields,
        fuzzy_fields=fuzzy_fields,
        page=params.page,
        per_page=params.perPage,
    )


@router.get("/{id}", response_model=WorkerPublic)
async def get_worker(session: SessionDep, id: int):
    worker = await Worker.one_by_id(session, id)
    if not worker:
        raise NotFoundException(message="worker not found")

    return worker


@router.post("", response_model=WorkerPublic)
async def create_worker(session: SessionDep, worker_in: WorkerCreate):
    existing = await Worker.one_by_field(session, "name", worker_in.name)
    if existing:
        raise AlreadyExistsException(message=f"worker f{worker_in.name} already exists")

    try:
        worker_in.compute_state()
        worker = await Worker.create(session, worker_in)
        return worker
    except Exception as e:
        raise InternalServerErrorException(message=f"Failed to create worker: {e}")


@router.put("/{id}", response_model=WorkerPublic)
async def update_worker(session: SessionDep, id: int, worker_in: WorkerUpdate):
    worker = await Worker.one_by_id(session, id)
    if not worker:
        raise NotFoundException(message="worker not found")

    try:
        worker_in.compute_state()
        await WorkerService(session).update(worker, worker_in)
    except Exception as e:
        raise InternalServerErrorException(message=f"Failed to update worker: {e}")

    return worker


@router.delete("/{id}")
async def delete_worker(session: SessionDep, id: int):
    worker = await Worker.one_by_id(session, id)
    if not worker:
        raise NotFoundException(message="worker not found")

    try:
        await WorkerService(session).delete(worker)
    except Exception as e:
        raise InternalServerErrorException(message=f"Failed to delete worker: {e}")
