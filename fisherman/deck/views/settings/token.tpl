% rebase('base.tpl')

<div class="container">
  <div class="row">
    <div class="col-xs-12">
      <h1 class="pull-left">Token</h1>
      <div class="pull-right"></div>
    </div>
  </div>
  <div class="row">
    <div class="col-xs-10">
      <form method="post">
        <div class="form-group">
          <label for="request-header">Token</label>
          <br>
          <textarea id="request-header" name="request-header" class="form-control" style="height: 340px">{{request_header}}</textarea>
        </div>
        <br>
        <br>
        <div class="form-group">
          <button type="submit" class="btn btn-primary">提交</button>
        </div>
      </form>
    </div>
  </div>
</div>
