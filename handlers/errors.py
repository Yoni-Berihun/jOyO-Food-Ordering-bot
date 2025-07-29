async def error_handler(update, context):
    import traceback
    print(f"Exception occurred:\n{traceback.format_exc()}")