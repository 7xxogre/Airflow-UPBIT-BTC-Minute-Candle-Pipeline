# Airflow를 통한 UPBIT KRW-BTC 분봉 데이터 적재 파이프라인

## 개요

최근 비트코인 가격이 급등함에 따라, 신뢰할 수 있는 최신의 금융 데이터를 적절히 확보하는 것이 중요해졌다.

이 프로젝트에서는 Airflow와 Upbit API를 사용하여 매일 오전 9시에 24시간 동안의 비트코인 가격 데이터를 자동으로 수집하여 MYSQL DB에 저장하는 자동화 파이프라인을 만드는 과정을 다룬다.



### 프로젝트 환경 설정 및 작업 내용

[[Airflow] 비트코인 일일 분 봉 데이터 파이프라인 프로젝트 (환경 설정편)](https://bestech49.tistory.com/54)

[[Airflow] 비트코인 일일 분 봉 데이터 파이프라인 프로젝트 (작업편)](https://bestech49.tistory.com/55)

### 환경

- **서버**: GCP e2-standard-2(2 CORE, MEMORY: 8G) DISK: 30G
- **운영체제**: UBUNTU 22.04 x86
- **Airflow 설치 방법**: Docker를 이용한 환경 구성
- **개발 환경**: Anaconda를 통한 가상 환경 관리, Jupyter Lab


### TODO

- 여러가지 Symbol에 대해서도 가능하도록 DAG 추가
- 1분봉 뿐만 아닌 5분, 10분 1시간 6시간 1일 봉 추가
