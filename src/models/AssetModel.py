from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId
from sqlalchemy.future import select
from sqlalchemy import func, delete

class AssettModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        isinstance = cls(db_client)
        return isinstance
                
    async def create_asset(self, asset: Asset):

        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            await session.commit()
            await session.refresh(asset)

        return asset

        return asset
    
    async def get_all_project_assets(self, asset_project_id: str, asset_type: str ):

        async with self.db_client() as session:
            query = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_type == asset_type
            )
            result = await session.execute(query)
            assets = result.scalars().all()

        return assets

    async def get_aseet_record(self, asset_project_id: str, asset_name: str ):

        async with self.db_client() as session:
            query = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_name == asset_name
            )
            result = await session.execute(query)
            asset = result.scalar_one_or_none()

        return asset

        