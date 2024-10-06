from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response
from fastapi import UploadFile
import  gc

from service.photo_service import PhotoService
from service.acne_service import AcneService

app_router = APIRouter()

@app_router.post('/report')
def post(
    request: Request,
    photo: UploadFile = Depends(PhotoService.validate_photo)
):
    acne_service = AcneService()
    last_model_keras_name = request.app.state.model_keras
    report = acne_service.get_acne_report(photo, last_model_keras_name)
    del acne_service
    gc.collect()
    return Response(str(report), 200)
