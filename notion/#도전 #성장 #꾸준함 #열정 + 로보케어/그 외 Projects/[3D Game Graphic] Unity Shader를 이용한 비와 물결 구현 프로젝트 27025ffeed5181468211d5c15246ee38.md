# [3D Game/Graphic] Unity Shader를 이용한 비와 물결 구현 프로젝트

상태: 3D Game

![그림2.png](%5B3D%20Game%20Graphic%5D%20Unity%20Shader%EB%A5%BC%20%EC%9D%B4%EC%9A%A9%ED%95%9C%20%EB%B9%84%EC%99%80%20%EB%AC%BC%EA%B2%B0%20%EA%B5%AC%ED%98%84%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/%25EA%25B7%25B8%25EB%25A6%25BC2.png)

**소개**

- **비 오는 거리를 주제로 가로수 길 배경, 물결, 비, 물의 파동, 반사, 물이 차오르는 애니메이션, 화면 일그러지는 효과 구현**

**기술 스택**

- Unity, C#, Shader

**업무 기간**

- 2019.10 ~ 2019.11 (약 2개월)

**역할**

- 기획 및 개발 (전체 기여도 100 %)

**배운 점**

- shader를 이용하여 사실적인 벽, 바닥 구현
- **_Scale * sin(_Time.w * _Speed * _Fre + (v.vertex.x + v.vertex.z))** 식을 이용하여 물결 구현
- **Fresnel 공식**(카메라를 바라보는 면이 밝고 카메라와 각도가 벌어질수록 어두워짐)을 이용하여 시점에 따른 **물의 깊이 변화를 구현**
- **Particle**을 이용하여 **비 및 작은 물결 구현**
- 떨어지는 공의 충돌 위치에 맞춰 **물리적인 물의 파동 구현**
- **Reflection Probe**를 이용하여 **물의 반사를 구현**
- 비가 와서 물이 서서히 차 오르는 효과 구현
- 빗방울 때문에 카메라 시야가 일그러지는 것을 **lmage effect shader** 표현

**관련 영상** 

[GameProgramming Project - 유니티 Shader를 이용한 비와 물결 구현(2)](https://youtu.be/uOzMHFREWpI)

**관련 링크**

- 더 세부적인 내용 참고 : [https://88-it.tistory.com/87](https://88-it.tistory.com/87)

---

[◀ 이전 페이지 돌아가기](../../#%EB%8F%84%EC%A0%84%20#%EC%84%B1%EC%9E%A5%20#%EA%BE%B8%EC%A4%80%ED%95%A8%20#%EC%97%B4%EC%A0%95%20+%20%EB%A1%9C%EB%B3%B4%EC%BC%80%EC%96%B4%2027025ffeed5180a29468cef3d3a5db17.md)