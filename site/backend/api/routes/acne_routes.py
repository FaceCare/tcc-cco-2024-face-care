from fastapi import APIRouter, Depends
from fastapi.responses import Response
from fastapi import UploadFile

from service.photo_service import PhotoService
from service.acne_service import AcneService

app_router = APIRouter()
acne_service = AcneService()

@app_router.post('/report')
def post(
    photo: UploadFile = Depends(PhotoService.validate_photo)
):
    report = acne_service.get_acne_report(photo)
    return Response(str(report), 200)
