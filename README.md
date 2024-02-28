유튜브 URL을 넣으면 음성을 인식하여 텍스트를 추출하는 프로그램입니다.

ffmpeg 설치가 선행되어야 합니다.

1. 유튜브 URL을 입력합니다
2. 저장될 폴더를 지정합니다
3. 작업을 진행합니다

model = whisper.load_model("large")
작업 모델의 경우 기본은 large로 등록 되어 있습니다.

모델 성능 비교

"tiny" 모델: 가장 작고 처리 속도가 가장 빠릅니다. 낮은 계산 자원에서 작동하기에 적합하지만, 정확도는 가장 낮습니다.

"base" 모델: "tiny"보다 크기와 정확도가 증가한 모델입니다. 빠른 처리 속도와 합리적인 정확도의 균형을 제공합니다. 경량화된 모델이면서도 다양한 음성 인식 작업에 충분히 사용될 수 있는 정확도를 제공합니다.

"small" 모델: "base"보다 더 나은 정확도를 제공하면서도 처리 속도는 비교적 빠른 편입니다. 중간 정도의 계산 자원을 가진 환경에서 사용하기 적합합니다.

"medium" 모델: 높은 정확도를 제공하지만 처리 속도가 느리고, 상당한 계산 자원을 요구합니다. 더 복잡한 음성 인식 작업에 적합합니다.

"large" 모델: 가장 크고 정확도가 가장 높은 모델입니다. 그러나 처리 속도가 가장 느리고 매우 많은 계산 자원을 소모합니다. 최상의 정확도가 필요한 경우에 선택합니다.


"base" 모델은 대부분의 사용자에게 권장되는 시작점입니다. 
이 모델은 좋은 성능과 합리적인 처리 속도를 제공하며, 대부분의 음성 인식 작업에 충분한 정확도를 제공합니다. 
필요에 따라 다른 모델로 전환하여 성능과 속도 사이의 최적의 균형을 찾아볼 수 있습니다.
