# SIH-2020
SIH 2020 project dt. Jan 06 2020

## Problem Statement
 ---------------------------------------------------------------------------------------------------------------------------
| Title 	| Content 	|
|---------------	|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| Descritption 	| Though there exists a technology for face recognition based authentication, dynamic human recognition based authentication is highly challenging. For a given entrance gate a hardware-software solution is needed to identify every unique person who enters or exit the gate, with log of all previous entry/exit time, photo/videos recorded. That means there will not be a previous history of an individual on the first entry. The system should immediately alert the security if it is a new person and the security will decide to allow/restrict that person entering inside the premises. Whereas, the system should learn from its previous history of videos/images dynamically to allow a known person. For a given size of the gate, the number of cameras with optimal resolution required is also to be worked out as part of solution. The solution should be scalable and preferably based open source. 	|
| Organization 	| Dte of IT & Cyber Security, DRDO 	|
| Category 	| Software 	|
| Domain Bucket 	| Security & Surveillance 	|

## Project Contents - prototype dt. Jan 06 2020

### Video Based Dynamic Face recognition
```bash
.
├── app.py
├── enroll.py
├── face_rec.py
├── faces
│   ├── Ajay
│   │   ├── 2020-01-06
│   │   │   ├── Ajay_19.jpg
│   │   │   ├── Ajay_20.jpg
│   │   │   └── Ajay_21.jpg
│   │   └── Enrollment_data
│   │       └── 2020-01-06 12:00:36.097371.avi
│   ├── Thamz
│   │   ├── 2020-01-05
│   │   │   ├── Thamz_96.jpg
│   │   │   ├── Thamz_97.jpg
│   │   │   └── Thamz_98.jpg
│   │   └── Enrollment_data
│   │       └── 2020-01-05 22:13:13.583251.avi
│   └── Vijay
│       ├── 2020-01-05
│       │   ├── Vijay_168.jpg
│       │   ├── Vijay_169.jpg
│       │   └── Vijay_170.jpg
│       └── Enrollment_data
│           └── 2020-01-05 21:32:29.462316.avi
├── haarcascade_frontalface_default.xml
├── __pycache__
│   ├── enroll.cpython-37.pyc
│   └── face_rec.cpython-37.pyc
└── unknownDetected
    ├── 1Unknown_Face.jpg
    ├── 2Unknown_Face.jpg
    └── 3Unknown_Face.jpg

12 directories, 21 files
```
