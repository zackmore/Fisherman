% rebase('base.tpl')

<div class="container">
  <h1>话题—微博列表</h1>
  <table class="table table-hover">
    <thead>
      <tr>
        <th>ID</th>
        <th>内容</th>
      </tr>
    </thead>
    <tbody>
      % for weibo in weibos:
        <tr>
          <td>{{weibo.id}}</td>
          <td>{{weibo.content}}</td>
        </tr>
      % end
    </tbody>
  </table>
  <div class="row">
    % include('pagination.tpl', pagination=pagination)
  </div>
</div>
