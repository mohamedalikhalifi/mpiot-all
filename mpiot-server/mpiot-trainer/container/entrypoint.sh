while [ ! -d '/service' ]; do
    sleep 10
done

cd /service
echo "staring  training service"
python -u encode_faces.py --dataset /uploads --encodings /shared/encodings.pickle --detection-method cnn


