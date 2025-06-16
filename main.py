if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:create_app",
        host="127.0.0.1",
        port=7860,
        reload=True,
        loop="asyncio",
    )
