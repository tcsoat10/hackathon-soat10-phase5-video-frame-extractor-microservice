from fastapi import APIRouter, status, Depends
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.presentation.api.v1.controllers.video_controller import VideoController
from src.core.domain.dtos.video_frame_extractor.register_video_dto import RegisterVideoDTO
from src.core.domain.dtos.video_frame_extractor.video_job_dto import VideoJobDTO

router = APIRouter()

@router.post(
    "/video/register",
    response_model=VideoJobDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registra um novo vídeo para processamento"
)
@inject
async def register_video(
    dto: RegisterVideoDTO = Depends(),
    controller: VideoController = Depends(Provide[Container.video_controller]),
):
    return await controller.register_video(dto)
