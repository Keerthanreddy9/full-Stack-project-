$(function(){
  // Bootstrap client-side validation
  (function() {
    'use strict'
    var forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms).forEach(function(form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add('was-validated')
      }, false)
    })
  })()

  // Stats page charts
  if($('#pieVisited').length){
    (async function(){
      const res = await fetch('/api/stats');
      const data = await res.json();

      new Chart(document.getElementById('pieVisited'), {
        type: 'pie',
        data: { 
          labels: ['Visited','Not Visited'], 
          datasets: [{ 
            data: [data.visited, data.not_visited], 
            backgroundColor: ['#14b8a6','#fb923c'] 
          }] 
        },
      });

      const labels = Object.keys(data.by_continent);
      const counts = Object.values(data.by_continent);
      new Chart(document.getElementById('barContinent'), {
        type: 'bar',
        data: { 
          labels, 
          datasets: [{ 
            label: 'Places', 
            data: counts, 
            backgroundColor: '#06b6d4'
          }] 
        },
        options: { scales: { y: { beginAtZero: true } } }
      });

      const pct = Math.round(data.completion_pct);
      const barEl = document.getElementById('progressBar');
      barEl.style.width = pct + '%';
      barEl.textContent = pct + '% Completed';
    })();
  }

  // Live search client-side filter to complement server-side
  $('#live-search').on('input', function(){
    const q = $(this).val().toLowerCase();
    $('#places-table tbody tr').each(function(){
      const name = $(this).data('name')+'';
      const country = $(this).data('country')+'';
      $(this).toggle(name.includes(q) || country.includes(q));
    });
  });

  // Toggle visited via AJAX
  $(document).on('click', '.toggle-visited', function(e){
    e.preventDefault();
    const id = $(this).data('id');
    const btn = $(this);
    $.post(`/toggle_visited/${id}`, {}, function(resp){
      if(resp.ok){
        // update row UI
        const row = btn.closest('tr');
        if(resp.visited){
          row.find('td:nth-child(6)').html(`<span class="badge bg-success">Visited<\/span><small class="text-muted d-block">${resp.visited_date}<\/small>`);
          btn.text('Mark Unvisited');
        } else {
          row.find('td:nth-child(6)').html(`<span class="badge bg-warning text-dark">Not Visited<\/span>`);
          btn.text('Mark Visited');
        }
        row.fadeOut(100).fadeIn(200);
      }
    });
  });

  // Delete confirmation modal
  let deleteId = null;
  const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
  $(document).on('click', '.btn-delete', function(){
    deleteId = $(this).data('id');
    $('#del-name').text($(this).data('name'));
    modal.show();
  });
  $('#confirm-delete').on('click', function(){
    if(!deleteId) return;
    $.ajax({
      url: `/delete/${deleteId}`,
      method: 'POST',
      headers: {'X-Requested-With': 'XMLHttpRequest'},
      success: function(){
        $(`button.btn-delete[data-id=${deleteId}]`).closest('tr').fadeOut(200, function(){ $(this).remove(); });
        modal.hide();
      }
    });
  });
});
