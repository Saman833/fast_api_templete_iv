import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep , GroupSer
from app.group.schema.group_schema import (
    GroupCreate,
    GroupPublic,
    GroupUpdate 
)
router = APIRouter(prefix="/group", tags=["group"])
@router.post("/", response_model=GroupPublic)
def create_group(*,current_user:CurrentUser ,group_service:GroupSer, group_create:GroupCreate):
    print ("im in create group" , 1000*"+")
    print("current user id , :" , current_user.id) 
    print ("current user id type : " , type(current_user.id))
    return group_service.create_new_group(owner_id=current_user.id,group_in=group_create) 


@router.get("/{id}" , response_model=GroupPublic)
def get_group(* , current_user:CurrentUser , id:uuid.UUID , group_service:GroupSer):
    return group_service.get_group_by_id(owner_id=current_user.id , group_id=id) 


@router.put("/{id}" , response_model=GroupPublic)
def update_group_info(current_user:CurrentUser , group_update:GroupUpdate , group_service:GroupSer):
    return group_service.update_group_by_id(owner_id=current_user.id , group_update=group_update)
     

    
