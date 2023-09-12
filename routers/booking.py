from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from crud.bookings import BookingCRUD
from models.booking import BookingOut, BookingIn


router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


@router.get('/', response_model=List[BookingOut], status_code=status.HTTP_200_OK)
def get_all(test_crud: BookingCRUD = Depends()):
    data = test_crud.read_all()
    return data


@router.get('/{test_id}', response_model=BookingOut, status_code=status.HTTP_200_OK)
def get_one(test_id: int,
            test_crud: BookingCRUD = Depends()):
    data = test_crud.read_one(test_id)
    return data


@router.post('/', response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create(test_data: BookingIn,
           test_crud: BookingCRUD = Depends()):
    data = test_crud.create(test_data.__dict__)
    return data


@router.delete('/{test_id}', response_model=BookingOut)
def delete(test_id: int,
           test_crud: BookingCRUD = Depends()):
    data = test_crud.read_one(test_id)
    test_crud.delete(data)
    return Response()
