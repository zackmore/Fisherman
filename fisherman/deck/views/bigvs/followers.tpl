% rebase('base.tpl')

<div class="container">
  <div class="row">
    <h1 class="pull-left">大 V 粉丝列表</h1>
    <div class="pull-right">
      % include('searchform.tpl')
    </div>
  </div>
  <table class="table table-hover">
    <thead>
      <tr>
        <th>ID</th>
        <th>Weibo ID</th>
        <th>名字</th>
        <th>链接</th>
        <th>创建于</th>
      </tr>
    </thead>
    <tbody>
      % for follower in followers:
        <tr>
            <td>{{follower.id}}</td>
            <td>{{follower.weibo_id}}</td>
            <td>{{follower.name}}</td>
            <td>{{follower.link}}</td>
            <td>{{follower.created_at}}</td>
        </tr>
      % end
    </tbody>
  </table>
  <div class="row">
    % include('pagination.tpl', pagination=pagination)
  </div>
</div>
