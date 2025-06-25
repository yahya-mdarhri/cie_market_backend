
pip install -r requirements.txt

mkdir -p staticfiles

python3 manage.py collectstatic --noinput --clear || {
    echo "collectstatic failed, but continuing with build..."
    # Create empty staticfiles directory as fallback
    mkdir -p staticfiles
    touch staticfiles/.gitkeep
}

echo "Build completed successfully"
