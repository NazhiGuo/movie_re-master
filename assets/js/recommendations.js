function fetchRecommendations(userId) {
    fetch('/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId })
    })
    .then(response => response.json())
    .then(data => {
      if (data.recommendations) {
        updateRecommendationsList(data.recommendations);
      } else {
        console.error(data.error || '无推荐数据');
      }
    })
    .catch(error => console.error('获取推荐数据出错:', error));
  }
  
  // 更新 HTML 中的推荐列表
  function updateRecommendationsList(recommendations) {
    const recommendationItems = document.querySelectorAll('#recommendations-list .product-item');
  
    recommendations.slice(0, 8).forEach((recommendation, index) => {
      const item = recommendationItems[index];
      const img = item.querySelector('.product-banner img');
      const title = item.querySelector('.product-title');
  
      img.src = `./assets/images/explore-product-${index + 1}.jpg`; // 假设每个电影有对应的图片
      img.alt = recommendation.title;
      title.textContent = `${index + 1} - ${recommendation.title}`; // 设置推荐序列标题
    });
  }
  
  // 调用函数获取推荐列表
  fetchRecommendations(1); // 替换为用户的实际 userId