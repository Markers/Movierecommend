# Movierecommend
Movie Recommend using ML

1. 데이터 가져오기 (BeautifulSoup)  

     연도별 : https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}&page=10000

    movie code 로 상세 정보 가져오기.

2. 데이터 저장  
   -  로컬 DB 저장.
   -  모델링 진행   

   
   docker 이용(M1 mac)
   ```
   docker run --rm --platform linux/amd64 -it mysql:5.7
   ```

3. API 서비스 개발

   - 간략한 GET, POST 1개씩 구현.

4. 대시보드 연동 => 플라스크 안에 대쉬보드 넣을 수 있도록

   - 대쉬보드 포트 관련 문제로 인한 연동 못함 -> 연동 방법 찾음. Metabase 구동 포트와 동일하게 하면 됨


해야될 일.
- [ ] 코드 OOP관점에서 다시 정리.
- [ ] 영화 데이터 수집시 Count 가 0으로 표기 되는 문제 확인
- [ ] DB 설계 제대로 하기 (정규화)
- [ ] Frontend 부분 공부해서 좀 더 꾸미기
- [ ] ML Model 더 좋은거 있는지 확인 및 성능 개선의 실마리 찾기
- [ ] 배포 관련해서 적절한 서비스 찾아서 공부해오기
   