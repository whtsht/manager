/**
 * Designer    : 小田桐光佑
 * Date        : 2023/6/
 * Purpose     :ログインをする前の機能概要やログインページへの誘導のためのwebページ
 */
import Button from "./line_login_bottun";
import nonlogin from "./images/nonLogin.jpg";
import qrCode from "./images/qrsample.jpeg";
import line2 from "./images/line2.jpg";
import line1 from "./images/line1.jpg";

function loggedOut() {
  const handleButtonClick = () => {
    /**
     * ここに実際のlineログインの処理を追加する．
     **/
    window.open("https://example.com/line-login");
  };

  return (
    <>
      <h1>予定管理をより 手軽に！</h1>
      <h2>アシスタントマネージャシステム</h2>
      <h2>Assistant Manager System</h2>
      <img src={nonlogin} />
      <h4>今すぐ下のQRコードから友達追加</h4>
      <img src={qrCode} />
      <Button
        border="none"
        color="blue"
        height="200px"
        onClick={handleButtonClick}
        radius="50%"
        width="200px"
        children="lineログインはここをクリック"
      />
      <h2>lineから予定と通知時間を登録すると...</h2>
      <img src={line1} />
      <h2>lineでお知らせしてくれる!</h2>
      <img src={line2} />
    </>
  );
}

export default loggedOut;
