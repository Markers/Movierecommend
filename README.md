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

4. 대시보드 연동 => 플라스크 안에 대쉬보드 넣을 수 있도록
   