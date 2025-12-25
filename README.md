# EL Management System

Experiential Learning Management System with AI-powered features, plagiarism detection, and advanced analytics.

## 🚀 Features

- **NLP-Based Auto-Assignment**: TF-IDF semantic similarity matching for faculty-theme assignment
- **Plagiarism Detection**: URL-based content fetching and similarity checking
- **Power BI Analytics**: Interactive dashboards with insights and recommendations
- **Project Health Monitoring**: AI-calculated health scores for projects
- **Real-time Search**: Search across students, faculty, projects, and mappings

## 📋 Prerequisites

- **Python** 3.8+
- **Node.js** 16+
- **MySQL** 8.0+
- **npm** or **yarn**

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd eldbms
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd el_project_backend
pip install -r requirements.txt
```

**Required packages:**
```bash
pip install flask flask-mysqldb flask-jwt-extended flask-cors python-dotenv beautifulsoup4 requests
```

#### Database Setup

1. **Create Database**:
   ```bash
   mysql -u root -p
   ```
   ```sql
   CREATE DATABASE eldb;
   USE eldb;
   ```

2. **Import Schema**:
   ```bash
   mysql -u root -p eldb < database_schema.sql
   ```

3. **Optional - Import Sample Data**:
   ```bash
   mysql -u root -p eldb < database_full_backup.sql
   ```

4. **Run Migrations**:
   ```bash
   mysql -u root -p eldb < db_migration.sql
   ```

#### Configure Environment

Create `.env` file in `el_project_backend/`:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=eldb
JWT_SECRET_KEY=your-secret-key-here
```

#### Run Backend

```bash
python run.py
```

Backend will run on: `http://localhost:5000`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd ../el-management-frontend
npm install
```

#### Configure API Endpoint

Update `src/pages/AdminDashboard.js` if needed:
```javascript
const API_BASE = 'http://localhost:5000';
```

#### Run Frontend

```bash
npm start
```

Frontend will run on: `http://localhost:3000`

## 👥 Default Credentials

After importing sample data, use these credentials:

**Admin:**
- Email: `admin@rvcoe.com`
- Password: `admin123`

**Faculty:**
- Email: `faculty@rvcoe.com`
- Password: `faculty123`

**Student:**
- Email: `student@rvcoe.com`
- Password: `student123`

## 📁 Project Structure

```
eldbms/
├── el_project_backend/          # Flask Backend
│   ├── your_app/
│   │   ├── admin/              # Admin routes
│   │   ├── auth/               # Authentication
│   │   ├── faculty/            # Faculty routes
│   │   └── student/            # Student routes
│   ├── database_schema.sql     # DB schema only
│   ├── database_full_backup.sql # DB with sample data
│   ├── db_migration.sql        # Latest migrations
│   └── run.py                  # Entry point
│
└── el-management-frontend/      # React Frontend
    ├── src/
    │   ├── components/         # Reusable components
    │   ├── pages/              # Dashboard pages
    │   ├── context/            # Auth context
    │   └── api/                # API calls
    └── public/
```

## 🔌 API Endpoints

### Admin
- `POST /admin/auto_assign` - AI-powered faculty assignment
- `GET /admin/insights` - Dashboard insights
- `GET /admin/analytics` - Analytics data
- `POST /admin/plagiarism/check` - Check submission plagiarism
- `GET /admin/submissions/all` - Get all submissions
- `GET /admin/themes/distribution` - Theme capacity analysis
- `GET /admin/mappings/student-mentor` - Student-mentor mappings
- `GET /admin/mappings/project-judge` - Project-judge mappings

### Authentication
- `POST /auth/register` - Register user
- `POST /auth/login` - Login
- `GET /auth/faculty/profile` - Get faculty profile
- `PUT /auth/faculty/interests` - Update faculty interests

## 🧪 Testing

### Test Plagiarism Detection

1. Go to Insights tab
2. Select a submission with URL content
3. Click "Check Plagiarism"
4. View similarity scores

### Test Auto-Assignment

1. Go to Assignments tab
2. Ensure faculty have interests set
3. Click "Run AI Auto-Assignment"
4. View assignment results with match scores

## 🐛 Troubleshooting

**Database Connection Error:**
- Check MySQL is running: `mysql -u root -p`
- Verify credentials in `.env`
- Ensure database exists: `SHOW DATABASES;`

**CORS Error:**
- Backend should have `flask-cors` installed
- Frontend API_BASE should match backend URL

**Module Not Found:**
```bash
pip install beautifulsoup4 requests
```

**Port Already in Use:**
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <pid> /F
```

## 📦 Deployment

### Backend (Python)
- Use **Heroku**, **Railway**, or **Render**
- Set environment variables
- Update `MYSQL_HOST` for cloud database

### Frontend (React)
- Use **Vercel**, **Netlify**, or **GitHub Pages**
- Update `API_BASE` to production backend URL
- Build: `npm run build`

### Database (MySQL)
- Use **AWS RDS**, **PlanetScale**, or **Railway**
- Import schema and data
- Update connection string

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is for educational purposes.

## 👨‍💻 Authors

- Keerthi Manne

## 🙏 Acknowledgments

- RV College of Engineering
- TailAdmin design inspiration
- NLP-based matching algorithms
