% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">话题—微博列表</h1>
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
            <th>用户</th>
            <th class="wrap">内容</th>
          </tr>
        </thead>
        <tbody>
          % for weibo in weibos:
            <tr>
              <td>{{weibo.id}}</td>
              <td><a class="_blank" href="{{weibo.user.link}}">{{weibo.user.name}}</a></td>
              <td class="wrap">{{weibo.content}}</td>
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
