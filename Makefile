.PHONY: install test lint format clean run

# 安装依赖
install:
	pip install -e .

# 运行测试
test:
	pytest

# 代码检查
lint:
	flake8 src tests
	black --check src tests
	isort --check-only src tests

# 格式化代码
format:
	black src tests
	isort src tests

# 清理缓存文件
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +

# 运行应用
run:
	python run.py

# 数据库迁移
migrate:
	alembic upgrade head

# 创建迁移
migrate-create:
	alembic revision --autogenerate -m "$(message)" 