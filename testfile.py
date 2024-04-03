from ultralytics import YOLO

def main():
    # Load a model
    model = YOLO('weights/yolov9c.pt')

    # Train the model
    results = model.train(data='data.yaml', batch = 8, epochs=100, imgsz=640, rect=True, device=0)

    results.show()

if __name__ == '__main__':
    main()

 # GPU %100 kullanıyor tüm değerler aynı 3070 Ti ile aralarında 3 kat eğitim süre farkı var. 30 dk iken, burada 1.30 saat sürdü.
 #