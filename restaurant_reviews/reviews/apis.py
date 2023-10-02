from flask import Blueprint, request, json, g
from dacite import from_dict
from dacite_config import config
from reviews import dataclasses, datahelper, errors
from results import make_data_result

blueprint = Blueprint("reviews", import_name = "reviews")


@blueprint.route('', methods=["POST"])
def add_review():
    #1. 解析JSON或參數
    x = json.loads(request.data)
    obj = from_dict(dataclasses.AddReview, x, config=config)
    #2. 驗證資料
    #2.1. restaurant_id是否存在
    if datahelper.is_restaurant_id_existed(obj.restaurant_id) == False:
        return json.jsonify(errors.e1001)
    #2.2. rating介於1~5之間
    if obj.rating < 1 or obj.rating > 5:
        return json.jsonify(errors.e1002)
    #2.3. comment<=45個字
    if obj.comment != None and len(obj.comment) > 45:
        return json.jsonify(errors.e1003)

    #3. 建立review
    #3.1. 建立review
    s = datahelper.create_review(obj.restaurant_id, obj.rating, obj.comment)
    #3.2. 提交
    g.cursor().connection.commit()
    #4. 回傳review
    return json.jsonify(make_data_result(s))


@blueprint.route('/<restaurant_id>', methods=["GET"])
def get_reviews(restaurant_id):
    #1. 解析JSON或參數
    #1.1. 解析restaurant_id為int
    try:
        restaurant_id = int(restaurant_id)
    except:
        return json.jsonify(errors.e2001)

    #2. 驗證資料
    #2.1. 驗證restaurant_id是否存在
    if  isinstance(restaurant_id, int) == False or \
          datahelper.is_restaurant_id_existed(restaurant_id) == False:
        return json.jsonify(errors.e2001)

    #3. 取得reviews
    s = datahelper.get_reviews(restaurant_id)
    #4. 回傳reviews
    return json.jsonify(make_data_result(s))


@blueprint.route('/stats/<restaurant_id>', methods=["GET"])
def get_reviews_stats(restaurant_id):
    #1. 解析JSON或參數
    #1.1. 解析restaurant_id為int
    try:
        restaurant_id = int(restaurant_id)
    except:
        return json.jsonify(errors.e3001)

    #2. 驗證資料
    #2.1. 驗證restaurant_id是否存在
    if  isinstance(restaurant_id, int) == False or \
          datahelper.is_restaurant_id_existed(restaurant_id) == False:
        return json.jsonify(errors.e3001)

    #3. 取得reviews的統計資料
    s = datahelper.get_reviews_stats(restaurant_id)
    #4. 回傳reviews的統計資料
    return json.jsonify(make_data_result({"avg_rating":s}))





@blueprint.route('/<review_id>', methods=["DELETE"])
def delete_review(review_id):
    # 1. 解析JSON或參數
    # 1.1. 解析review_id為int
    try:
        review_id = int(review_id)
    except:
        return json.jsonify(errors.e4001)
    
    
    #2. 驗證資料
    #2.1. 驗證review_id是否存在
    if  isinstance(review_id, int) == False or \
          datahelper.is_review_id_existed(review_id) == False:
        return json.jsonify(errors.e4001) 
    #3. 刪除資料
    #3.1. 刪除資料
    success = datahelper.delete_review(review_id)
    #3.2. 提交
    g.cursor().connection.commit()
    #4. 回傳是否成功刪除
    return json.jsonify(make_data_result({"success":success}))