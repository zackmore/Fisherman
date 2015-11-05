% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">话题列表</h1>
      <div class="pull-right">
        % include('searchform.tpl')
      </div>
    </div>
  </div>
  <div class="row auto-overflow">
    <div class="col-xs-12">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>ID</th>
            <th>话题</th>
            <th>上次抓取时间</th>
            <th>创建于</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          % for topic in topics:
            <tr>
              <td>{{topic.id}}</td>
              <td><a target="_blank" href="//huati.weibo.com/k/{{topic.name[1:-1]}}">{{topic.name}}</a></td>
              <td>{{topic.last_fetched_at}}</td>
              <td>{{topic.created_at}}</td>
              <td>
                <a href="/fetch/topic/{{topic.id}}" class="btn btn-xs btn-warning fetch-topic">Fetch</a>
                <a href="/topics/users?topic_id={{topic.id}}" class="btn btn-xs btn-primary">相关用户</a>
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
