# api/routes.py
from fastapi       import APIRouter
from api.schemas   import SumInput, PlotInput
from api.processor import compute_sum, generate_plot

router = APIRouter()

@router.post("/process-data/sum")
def get_sum(data: SumInput):
    total = compute_sum(data.y)
    return {"sum": total}

@router.post("/process-data/plot")
def get_plot(data: PlotInput):
    encoded_plot = generate_plot(data.x, data.y)
    return {"plot_base64": encoded_plot}


from fastapi       import UploadFile, File, HTTPException
from api.schemas   import URLInput
from api.processor import parse_uploaded_file, parse_remote_file, compute_sum, generate_plot

@router.post("/upload-file")  # pip install python-multipart
async def upload_file(file: UploadFile = File(...)):
    try:
        x, y = parse_uploaded_file(file)
        return {
            "sum": compute_sum(y),
            "plot_base64": generate_plot(x, y)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/fetch-file")
def fetch_file(input: URLInput):
    try:
        x, y = parse_remote_file(input.url)
        return {
            "sum": compute_sum(y),
            "plot_base64": generate_plot(x, y)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Enter by Hand
from api.schemas   import TextInput
from api.processor import parse_text_input

@router.post("/manual-entry")
def manual_entry(data: TextInput):
    try:
        x, y = parse_text_input(data.text)
        return {
            "sum": compute_sum(y),
            "plot_base64": generate_plot(x, y)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
