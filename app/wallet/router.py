from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.wallet.schemas import AddressRequest, AddressResponse, LogResponse
from app.wallet.models import RequestLog
import tronpy.async_tron as async_tron
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.connection import get_db


wallet_router = APIRouter(prefix="/wallet", tags=["Wallet"])


@wallet_router.post("/info", response_model=AddressResponse)
async def get_address_info(req: AddressRequest, db: AsyncSession = Depends(get_db)):
    client = async_tron.AsyncTron()
    try:
        account = await client.get_account(req.address)
        balance = account.get('balance', 0) / 1_000_000
        bandwidth = account.get('free_net_usage', 0)
        energy = account.get('energy_usage', 0)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    log_entry = RequestLog(address=req.address)
    db.add(log_entry)
    await db.commit()

    return AddressResponse(
        address=req.address,
        balance_trx=balance,
        bandwidth=bandwidth,
        energy=energy,
    )

@wallet_router.get("/logs", response_model=List[LogResponse])
async def get_logs(skip: int = Query(0), limit: int = Query(10), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RequestLog).order_by(RequestLog.timestamp.desc()).offset(skip).limit(limit))
    logs = result.scalars().all()
    return logs