from app import tasks
import logging

async def dispatch_task(tool_name: str, args: dict):
    """
    Executes the appropriate task function based on the tool name.
    """
    logging.info(f"Dispatching task: {tool_name} with args: {args}")
    
    tool_map = {
        "install_uv_datagen": tasks.install_uv_datagen,
        "format_markdown": tasks.format_markdown,
        "count_weekdays": tasks.count_weekdays,
        "sort_json": tasks.sort_json,
        "extract_recent_logs": tasks.extract_recent_logs,
        "create_index": tasks.create_index,
        "extract_email_sender": tasks.extract_email_sender,
        "extract_credit_card": tasks.extract_credit_card,
        "find_similar_comments": tasks.find_similar_comments,
        "query_database": tasks.query_database
    }
    
    func = tool_map.get(tool_name)
    if not func:
        raise ValueError(f"Tool '{tool_name}' not implemented.")
        
    # Call the function with unpacked arguments
    return await func(**args)