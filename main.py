"""
Main module for handling FastAPI endpoints and dependencies related to the blockchain.
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import blockchain as _blockchain

app = FastAPI()


class BlockData(BaseModel):
    """Model for block data input."""

    data: str


def get_blockchain():
    """
    Provides an instance of the Blockchain.
    Checks if the blockchain is valid and raises an HTTPException if not.
    """
    blockchain = _blockchain.Blockchain()
    if not blockchain.is_chain_valid():
        raise HTTPException(status_code=400, detail="The blockchain is invalid")
    return blockchain


@app.post("/mine_block/")
def mine_block(
    block_data: BlockData, blockchain: _blockchain.Blockchain = Depends(get_blockchain)
):
    """Mines a block with the provided data and returns the new block."""
    return blockchain.mine_block(data=block_data.data)


@app.get("/blockchain/")
def get_blockchain_route(blockchain: _blockchain.Blockchain = Depends(get_blockchain)):
    """Returns the entire blockchain."""
    return blockchain.chain

# pylint: disable=unused-argument
@app.get("/validate/")
def is_blockchain_valid(blockchain: _blockchain.Blockchain = Depends(get_blockchain)):
    """Checks if the blockchain is valid and returns a relevant message."""
    return {"message": "The blockchain is valid."}


@app.get("/blockchain/last/")
def previous_block(blockchain: _blockchain.Blockchain = Depends(get_blockchain)):
    """Returns the last block in the blockchain."""
    return blockchain.get_previous_block()
