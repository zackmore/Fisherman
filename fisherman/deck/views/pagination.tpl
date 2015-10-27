<div class="col-xs-12">
    <nav>
      <ul class="pagination">
        % if pagination['has_prev']:
        <li>
          <a href="{{pagination['prev']}}" aria-label="Previous">
            <span aria-hidden="true">&laquo; 上一页</span>
          </a>
        </li>
        % end
        % if pagination['has_next']:
        <li>
          <a href="{{pagination['next']}}" aria-label="Next">
            <span aria-hidden="true">下一页 &raquo;</span>
          </a>
        </li>
        % end
      </ul>
    </nav>
</div>
