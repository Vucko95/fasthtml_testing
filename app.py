from fasthtml.common import *
from monsterui.all import *
import httpx
from pydantic import BaseModel
hdrs = Theme.stone.headers()
app, rt = fast_app(hdrs=hdrs)

sidebar = Form(
    Div(
        H3("SideBar"),
        DividerLine()
    )
)

class FormData(BaseModel):
    prefix: str
    owner: str
    aws_region: str
    ecs: str
    cm: str
    cdh: str
    ecs_parcel: str


def ex_form():
    return Card(Div(
        DivCentered(H3("One Node Cluster Setup")),
        Form(cls="space-y-4", hx_post="/submit", hx_target="#response")(
            Grid(
                LabelInput("Prefix", id="prefix", name="prefix"),
                LabelInput("Owner", id="owner", name="owner"),
                LabelSelect(
                    map(Option, ["eu-west-1", "us-east-2", "us-west-1"]),
                    label="AWS Region",
                    id="aws_region",
                    name="aws_region",
                ),
                LabelSelect(
                    map(Option, ["enable", "disable"]),
                    label="ECS",
                    id="ecs",
                    name="ecs",
                ),
            ),
            Grid(
                LabelSelect(
                    map(Option, ["1.1", "1.2", "1.3"]),
                    label="CM PARCEL",
                    id="cm",
                    name="cm",
                ),
                LabelSelect(
                    map(Option, ["1.1", "1.2", "1.3"]),
                    label="CDH PARCEL",
                    id="cdh",
                    name="cdh",
                ),
                LabelSelect(
                    map(Option, ["1.1", "1.2", "1.3"]),
                    label="ECS PARCEL",
                    id="ecs_parcel",
                    name="ecs_parcel",
                ),
            ),
            DivCentered(Button("Submit Form", cls=ButtonT.primary)),
        ),
        Div(id="response"),
    )
    )
# UploadZone(DivCentered(Span("Upload LICENSE"), UkIcon("upload")), id='upload2'),
# UploadZone(DivCentered(Span("Upload SSH KEY"), UkIcon("upload")), id='upload3'),

# def ex_form_credentials():
#     return Card(Div()(
#         DivCentered(H3("Key Creds")),
#         Form(cls="space-y-4", hx_post="/upload_file", hx_target="#response", enctype="multipart/form-data")(
#             Grid(
#                 UploadZone(DivCentered(Span("Upload AWS CREDS"), UkIcon("key")), id='upload1', name="file"),
#             ),
#             DivCentered(Button("Upload File", cls=ButtonT.primary)),
#         ),
#         Div(id="response"),
#     ))


@rt
def index():
    return Div(cls="grid grid-cols-6 h-screen")(
        Div(sidebar, cls="col-span-1 p-4 h-full border-r-2 border-gray-300"),
        Div(cls="col-span-4 flex flex-col  items-center")(
            Div(ex_form(), cls="p-6"),
            # Div(ex_form_credentials(), cls="p-6"),
            ex_upload()
        ),
    )

serve(reload=True)


@app.post("/submit")
async def submit_form(form_data: FormData):
    data = form_data.model_dump()
    print(type(data))

    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8002/receive", json=data)

    return Toast(DivLAligned(UkIcon('check-circle', cls='mr-2'), "Environment is starting to deploy"), id="success-toast", alert_cls=AlertT.success, cls=(ToastHT.end, ToastVT.bottom)),
    # return P(f"You are missing *** Credential", cls="text-error")
from fastapi import FastAPI, UploadFile, File

# async def upload_file(file: UploadFile = File(None)):
@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    # Await to read the content from the file
    content = await file.read()  # This will read the content and return bytes

    # Now decode the bytes into a string (assuming UTF-8 encoding)
    text_content = content.decode("utf-8")

    # Print to debug
    print(f"File content: {text_content}")

    # Return filename and content as a response
    return {"filename": file.filename, "content": text_content}


def ex_upload():
    return Card(Div(
        DivCentered(H3("Upload Credentials")),
        Form(cls="space-y-4", hx_post="/upload_file", hx_target="#upload_response", enctype="multipart/form-data")(
            Grid(
                UploadZone(DivCentered(Span("Upload AWS CREDS"), UkIcon("key")), id='upload1', name="file"),
            ),
            DivCentered(Button("Upload File", cls=ButtonT.primary)),
        ),
        Div(id="upload_response"),
    ))
