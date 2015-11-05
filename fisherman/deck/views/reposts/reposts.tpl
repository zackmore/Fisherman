% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">转发微博列表</h1>
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
            <th>原微博地址</th>
            <th>内容</th>
            <th>转发数</th>
            <th>上次抓取时间</th>
            <th>创建于</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          % for repost in reposts:
            <tr>
              <td>{{repost.id}}</td>
              <td>
                <a href="{{repost.base_url}}" target="_blank">{{repost.base_url}}</a>
              </td>
              <td class="wrap">{{repost.content}}</td>
              <td>{{repost.repost_count}}</td>
              <td>{{repost.last_fetched_at}}</td>
              <td>{{repost.created_at}}</td>
              <td>
                <a href="/reposts/users?repost_id={{repost.id}}" class="btn btn-xs btn-primary">参与转发用户</a>
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
