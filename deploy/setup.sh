#!/usr/bin/env bash
# HAFSQuiz OCI 서버 최초 설치 스크립트
# 실행: bash deploy/setup.sh
set -e

REPO_DIR="$HOME/HAFSQuiz"
cd "$REPO_DIR"

echo "=== [1/5] 시스템 패키지 설치 ==="
sudo apt-get update -q
sudo apt-get install -y -q python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

echo "=== [2/5] Python 가상환경 생성 및 의존성 설치 ==="
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt gunicorn --quiet

echo "=== [3/5] nginx 설정 (HTTP-only, SSL은 certbot이 추가) ==="
# SSL 인증서가 아직 없으므로 HTTP-only로 먼저 설정
# certbot --nginx 실행 시 자동으로 HTTPS 블록이 추가됨
sudo tee /etc/nginx/sites-available/hafsquiz > /dev/null << 'NGINXEOF'
server {
    listen 80;
    server_name hafsquiz.duckdns.org;

    client_max_body_size 10M;

    location /static/ {
        alias /home/ubuntu/HAFSQuiz/static/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINXEOF
# static 경로를 실제 홈으로 치환
sudo sed -i "s|/home/ubuntu/HAFSQuiz|$REPO_DIR|g" /etc/nginx/sites-available/hafsquiz
sudo ln -sf /etc/nginx/sites-available/hafsquiz /etc/nginx/sites-enabled/hafsquiz
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

echo "=== [4/5] systemd 서비스 설치 ==="
# 경로를 실제 홈 디렉토리로 치환
sed "s|/home/ubuntu|$HOME|g" deploy/hafsquiz.service | \
  sed "s|User=ubuntu|User=$(whoami)|g" | \
  sudo tee /etc/systemd/system/hafsquiz.service > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable hafsquiz

echo "=== [5/5] quizzes 디렉토리 확인 ==="
mkdir -p "$REPO_DIR/quizzes"

echo ""
echo "========================================"
echo "  설치 완료!"
echo "========================================"
echo ""
echo "다음 단계:"
echo "  1. cp .env.example .env && nano .env"
echo "     (SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET 입력)"
echo ""
echo "  2. sudo certbot --nginx -d hafsquiz.duckdns.org"
echo ""
echo "  3. sudo systemctl start hafsquiz"
echo "     sudo systemctl status hafsquiz"
echo ""
