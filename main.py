from flask import Flask, jsonify

from utils import create_bs, content_handle, make_updated_contest_data_list, make_notification_text, slack_api_post
from conf import TARGET_URL, PARSER, SLACK_NOTIFICATION

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=["GET"])
def index():
    try:
        bs = create_bs(TARGET_URL, PARSER)
        table = bs.find('div', attrs={'id': 'contest-table-upcoming'})\
            .find('table', attrs={'class': 'table'})\
            .find('tbody')
        contest_data_list = content_handle(table.contents)
        updated_contest_data_list = make_updated_contest_data_list(contest_data_list)
        is_updated = bool(len(updated_contest_data_list))
        if is_updated:
            notification_text = make_notification_text(updated_contest_data_list)
            slack_api_post(SLACK_NOTIFICATION, notification_text)
        return jsonify({'message': '成功'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'エラーが発生しました'}), 400


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
