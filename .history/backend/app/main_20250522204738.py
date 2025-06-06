from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from .core.middleware import setup_middlewares

# Create FastAPI app
app = FastAPI(
    title="MediScan AI",
    description="Early Disease Detection Through Multi-modal Medical Imaging Analysis",
    version="0.1.0",
)

# Set up security middleware
setup_middlewares(app)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to MediScan AI API",
        "status": "active",
        "version": "0.1.0"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
from .api.routes import auth_router, xray_router, mri_router, ct_router, report_router

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(xray_router, prefix="/api/xray", tags=["X-Ray Analysis"])
app.include_router(mri_router, prefix="/api/mri", tags=["MRI Analysis"])
app.include_router(ct_router, prefix="/api/ct", tags=["CT Scan Analysis"])
app.include_router(report_router, prefix="/api/report", tags=["Report Analysis"])

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    ) 
