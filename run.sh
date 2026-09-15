#后端
cd backend
uvicorn main:app --reload
#celery
cd backend
celery -A celery_app worker --loglevel=info
#前端
cd frontend
npm run dev -- --host 0.0.0.0 --port 5173
