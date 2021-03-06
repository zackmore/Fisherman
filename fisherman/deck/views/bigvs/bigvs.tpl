% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">大 V 列表</h1>
      <div class="pull-right">
        % include('searchform.tpl')
      </div>
    </div>
  </div>
  <br>
  <div class="row">
      <div class="col-xs-12">
          <a href="/im?weibo_ids=" class="im btn btn-primary">统一私信</a>
      </div>
  </div>
  <br>
  <br>
  <div class="row auto-overflow">
    <div class="col-xs-12">
      <table class="table table-hover">
        <thead>
          <tr>
            <th><input type="checkbox">&nbsp;全选</th>
            <th>ID</th>
            <th>Weibo ID</th>
            <th>名字</th>
            <th>链接</th>
            <th>创建于</th>
            <th>上次抓取于</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          % for bigv in bigvs:
            <tr>
                <td><input type="checkbox" value="{{bigv.weibo_id}}"></td>
                <td>{{bigv.id}}</td>
                <td>{{bigv.weibo_id}}</td>
                <td>{{bigv.name}}</td>
                <td>{{bigv.link}}</td>
                <td>{{bigv.created_at}}</td>
                <td>{{bigv.last_fetched_at}}</td>
                <td>
                    <a href="/im?weibo_ids={{bigv.weibo_id}}" class="btn btn-xs btn-primary">私信</a>
                    <a href="/bigvs/followers?bigv_id={{bigv.id}}" class="btn btn-xs btn-primary">粉丝</a>
                </td>
            </tr>
          % end
        </tbody>
      </table>
    </div>
  </div>
  <div class="row">
    % include('pagination.tpl', pagination=pagination)
  </div>
</div>
