% rebase('base.tpl')

<div class="container">
  <h1>转发微博列表</h1>
  <table class="table table-hover">
    <thead>
      <tr>
        <th>ID</th>
        <th>原微博地址</th>
        <th>内容</th>
        <th>转发数</th>
        <th>上次抓取时间</th>
        <th>创建于</th>
      </tr>
    </thead>
    <tbody>
      % for repost in reposts:
        <tr>
          <td>{{repost.id}}</td>
          <td>{{repost.base_url}}</td>
          <td>{{repost.content}}</td>
          <td>{{repost.repost_count}}</td>
          <td>{{repost.last_fetched_at}}</td>
          <td>{{repost.created_at}}</td>
        </tr>
      % end
    </tbody>
  </table>
</div>
