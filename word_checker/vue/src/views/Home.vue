<template>
  <div class="cover">
    <div class="cover-main">
      <img src="@/assets/logo.svg" alt="drawing" style="width: 200px;">
      <blockquote>
        <p>WordChecker</p>
      </blockquote>
      <ul>
        <li>易用的可研报告检测软件</li>
        <li>简单</li>
        <li>强大</li>
      </ul>
      <p>
        <a href="upload" rel="noopener">Get Started</a>
      </p>
    </div>
  </div>
</template>

<style scoped lang="scss">
$bodyFontSize: 17px;
$textColor: #34495e;
$siteFont: PT Sans;
$accent: #42b983;
$coverBackground: linear-gradient(to left bottom, hsl(118, 100%, 85%) 0%, hsl(181, 100%, 85%) 100%);

.cover {
  display: flex;
  align-items: center;
  background: $coverBackground !important;
  height: 100vh;

  color: $textColor;
  font-family: $siteFont, Helvetica Neue, Arial, sans-serif;
  font-size: $bodyFontSize;
}

.cover .cover-main {
  flex: 1;
  margin: -20px 16px 0;
  text-align: center;
  z-index: 1;
}

.cover blockquote {
  font-size: 1.5rem;
  text-align: center;
}

.cover p {
  line-height: 1.5rem;
  margin: 1em 0;
}

.cover ul {
  line-height: 1.8;
  list-style-type: none;
  margin: 1em auto;
  max-width: 500px;
  padding: 0;
}

.cover .cover-main p a {
  border-radius: 2rem;
  border: 1px solid $accent;
  box-sizing: border-box;
  display: inline-block;
  font-size: 1.05rem;
  letter-spacing: 0.1rem;
  margin: 0.5rem 1rem;
  padding: 0.75em 2rem;
  text-decoration: none;
  transition: all 0.15s ease;
  background-color: $accent;
  color: #fff;

  &:hover {
    color: inherit;
    opacity: .8;
  }
}
</style>