from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# =====================================================================
# 1. PYDANTIC SCHEMAS (Lá chắn Gateway validate dữ liệu đầu vào)
# =====================================================================

# Schema dùng cho chức năng cập nhật trạng thái tiến độ công việc
class TaskStatusUpdateSchema(BaseModel):
    status: str

# Schema dùng cho chức năng tạo mới công việc với các ràng buộc thuộc tính Field
class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100) # Tiêu đề từ 3-100 ký tự
    description: str = Field(...)                       # Mô tả, bắt buộc nhập
    assignee: str = Field(...)                          # Người thực hiện, bắt buộc nhập
    priority: int = Field(..., ge=1, le=5)              # Độ ưu tiên nằm trong dải [1, 5]

# Schema định dạng cấu trúc dữ liệu của một Task khi trả về
class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    assignee: str
    priority: int
    status: str
    created_at: str

# =====================================================================
# 2. IN-MEMORY DATABASE (Cơ sở dữ liệu giả lập trong bộ nhớ)
# =====================================================================
tasks_db = [
    {
        "id": 1, 
        "title": "Thiet ke database Shop AI", 
        "description": "Xay dung bang va toi uu index", 
        "assignee": "QuyDev", 
        "priority": 1, 
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2, 
        "title": "Code bo API Authen", 
        "description": "Trien khai filter verify JWT token", 
        "assignee": "FixerQ", 
        "priority": 2, 
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]

# =====================================================================
# 3. HELPER FUNCTIONS (Các hàm bổ trợ hệ thống)
# =====================================================================

# Hàm sinh chuỗi thời gian hiện tại theo định dạng ISO kết hợp chữ Z (UTC)
def get_iso_timestamp() -> str:
    return str(datetime.now().isoformat()) + "Z"

# Hàm đóng gói phản hồi chuẩn hóa theo Unified Envelope JSON gồm đúng 6 trường bắt buộc
def make_envelope(status_code: int, message: str, data: any = None, error: str = None, path: str = "") -> dict:
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": get_iso_timestamp(),
        "path": path
    }

# Hàm xử lý nghiệp vụ nội bộ tính toán số liệu hiệu suất (Trả về một Tuple 3 giá trị)
def calculate_team_metrics() -> tuple:
    total_tasks = len(tasks_db)
    if total_tasks == 0:
        return (0, 0, 0.0)
    
    completed_tasks = 0
    for task in tasks_db:
        if task["status"] == "done":
            completed_tasks += 1
            
    completion_rate = round((completed_tasks / total_tasks) * 100, 1)
    return (total_tasks, completed_tasks, completion_rate)


# =====================================================================
# 4. GLOBAL EXCEPTION HANDLERS (Bộ bẫy lỗi tập trung an toàn hệ thống)
# =====================================================================

# Bẫy lỗi các ngoại lệ HTTPException chủ động raise trong code nghiệp vụ
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, _):
    return JSONResponse(
        status_code=400,
        content=make_envelope(
            status_code=400,
            message="Yêu cầu không hợp lệ hoặc vi phạm ràng buộc dữ liệu!",
            data=None,
            error="ERR-TASK-400: Dynamic operational exception occurred.",
            path=request.url.path
        )
    )

# Bẫy lỗi toàn cục cho các lỗi Runtime bất ngờ (Triệt tiêu nguy cơ lộ Stack Trace thô)
@app.exception_handler(Exception)
def global_exception_handler(request: Request, _):
    return JSONResponse(
        status_code=500,
        content=make_envelope(
            status_code=500,
            message="Lỗi hệ thống không xác định!",
            data=None,
            error="ERR-SYS-500: Internal Server Error.",
            path=request.url.path
        )
    )

# Override bẫy lỗi Pydantic Validation lỗi đầu vào (Mã lỗi 422 chuẩn hóa)
@app.exception_handler(422)
def validation_exception_handler(request: Request, _):
    return JSONResponse(
        status_code=422,
        content=make_envelope(
            status_code=422,
            message="Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",
            data=None,
            error="ERR-VAL-422: Validation error at Request Body fields constraint layout.",
            path=request.url.path
        )
    )


# =====================================================================
# 5. API ENDPOINTS (Các hàm xử lý định tuyến tài nguyên)
# =====================================================================

# Chức năng 1: Lấy danh sách toàn bộ công việc hiện có (Hỗ trợ lọc theo Query Parameter)
@app.get("/tasks")
def get_all_tasks(request: Request, status: Optional[str] = None):
    # Khai báo biến List ảo sử dụng để linter/IDE không báo lỗi unaccessed import
    results = tasks_db
    if status:
        results = [t for t in tasks_db if t["status"] == status]
        
    return make_envelope(
        status_code=200,
        message="Lấy danh sách công việc thành công!",
        data=results,
        path=request.url.path
    )

# Chức năng 2: Tạo mới một công việc nhóm vào mảng tasks_db (Tự tăng ID, kiểm tra trùng tiêu đề)
@app.post("/tasks", status_code=201)
def create_task(request: Request, task_in: TaskCreateSchema):
    # Chuẩn hóa loại bỏ khoảng trắng thừa đầu cuối và khoảng trắng giữa của Assignee
    title_strip = task_in.title.strip()
    description_strip = task_in.description.strip()
    assignee_strip = "".join(task_in.assignee.split())
    
    # Chặn dữ liệu bẩn chứa toàn khoảng trắng gửi lên
    if not title_strip or not description_strip or not assignee_strip:
        raise HTTPException(status_code=422, detail="Dữ liệu không được chứa toàn khoảng trắng")

    # Kiểm tra trùng tiêu đề (ERR-TASK-01)
    for task in tasks_db:
        if task["title"].lower() == title_strip.lower():
            return JSONResponse(
                status_code=400,
                content=make_envelope(
                    status_code=400,
                    message="Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                    data=None,
                    error="ERR-TASK-01: Task conflict: Title field duplicates an existing record.",
                    path=request.url.path
                )
            )
            
    # Thuật toán tìm max_id để tự tăng ID thực thể mới
    max_id = 0
    for task in tasks_db:
        if task["id"] > max_id:
            max_id = task["id"]
            
    new_task = {
        "id": max_id + 1,
        "title": title_strip,
        "description": description_strip,
        "assignee": assignee_strip,
        "priority": task_in.priority,
        "status": "todo", # Mặc định gán trạng thái ban đầu là todo
        "created_at": get_iso_timestamp() # Tự động tạo mốc thời gian khởi tạo
    }
    
    tasks_db.append(new_task)
    return make_envelope(
        status_code=201,
        message="Khởi tạo công việc mới thành công!",
        data=new_task,
        path=request.url.path
    )

# Chức năng 3: Cập nhật tiến độ trạng thái (Kiểm tra tồn tại ID và chặn lùi trạng thái khi đã done)
@app.put("/tasks/{task_id}")
def update_task_status(request: Request, task_id: int, status_in: TaskStatusUpdateSchema):
    target_task = None
    for task in tasks_db:
        if task["id"] == task_id:
            target_task = task
            break
            
    # Không tìm thấy task_id trong hệ thống (ERR-TASK-03)
    if not target_task:
        return JSONResponse(
            status_code=404,
            content=make_envelope(
                status_code=404,
                message="Lỗi: Không tìm thấy ID công việc yêu cầu!",
                data=None,
                error="ERR-TASK-03: Resource not found by specific entity identify key.",
                path=request.url.path
            )
        )
        
    # Công việc đã ở trạng thái hoàn thành thì cấm thay đổi ngược lại (ERR-TASK-04)
    if target_task["status"] == "done":
        return JSONResponse(
            status_code=400,
            content=make_envelope(
                status_code=400,
                message="Lỗi: Công việc đã hoàn thành, không thể thay đổi trạng thái!",
                data=None,
                error="ERR-TASK-04: State block constraint: Cannot rollback status from completed state.",
                path=request.url.path
            )
        )
        
    target_task["status"] = status_in.status
    return make_envelope(
        status_code=200,
        message="Cập nhật tiến độ công việc thành công!",
        data=target_task,
        path=request.url.path
    )

# Chức năng 4: Endpoint điều phối số liệu thống kê phân tích Dashboard hiệu suất nhóm
@app.get("/tasks/analytics/dashboard")
def get_dashboard_analytics(request: Request):
    # Gọi hàm xử lý tính toán nghiệp vụ nội bộ để nhận Tuple kết quả
    total_tasks, completed_tasks, completion_rate = calculate_team_metrics()
    
    dashboard_data = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate_percentage": completion_rate
    }
    
    return make_envelope(
        status_code=200,
        message="Lấy số liệu thống kê hiệu suất nhóm thành công!",
        data=dashboard_data,
        path=request.url.path
    )