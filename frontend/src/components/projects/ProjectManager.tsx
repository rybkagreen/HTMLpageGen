'use client';

import { Project, ProjectManager } from '@/lib/project-manager';
import { cn } from '@/lib/utils';
import { AnimatePresence, motion } from 'framer-motion';
import {
  Calendar,
  Clock,
  Copy,
  Download,
  Eye,
  FileText,
  Plus,
  Search,
  Trash2,
  Upload,
} from 'lucide-react';
import { useEffect, useState } from 'react';

interface ProjectManagerProps {
  onProjectSelect?: (project: Project) => void;
  onProjectCreate?: () => void;
  className?: string;
}

interface ProjectStats {
  totalProjects: number;
  totalFiles: number;
  totalSize: number;
  projectsByType: Record<string, number>;
  recentActivity: Array<{ date: string; count: number }>;
}

export default function ProjectManagerComponent({
  onProjectSelect,
  onProjectCreate,
  className,
}: ProjectManagerProps) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [filteredProjects, setFilteredProjects] = useState<Project[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'name' | 'date' | 'type'>('date');
  const [isLoading, setIsLoading] = useState(true);
  const [stats, setStats] = useState<ProjectStats | null>(null);
  const [showStats, setShowStats] = useState(false);

  const projectManager = new ProjectManager();

  useEffect(() => {
    loadProjects();
    loadStats();
  }, []);

  useEffect(() => {
    filterAndSortProjects();
  }, [projects, searchQuery, selectedType, sortBy]);

  const loadProjects = async () => {
    setIsLoading(true);
    try {
      const loadedProjects = await projectManager.getAllProjects();
      setProjects(loadedProjects);
    } catch (error) {
      console.error('Error loading projects:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const projectStats = await projectManager.getStats();
      setStats(projectStats);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const filterAndSortProjects = () => {
    let filtered = projects;

    // Фильтрация по поиску
    if (searchQuery) {
      filtered = filtered.filter(
        project =>
          project.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          project.metadata.description
            .toLowerCase()
            .includes(searchQuery.toLowerCase()) ||
          project.metadata.tags.some(tag =>
            tag.toLowerCase().includes(searchQuery.toLowerCase())
          )
      );
    }

    // Фильтрация по типу
    if (selectedType !== 'all') {
      filtered = filtered.filter(project => project.type === selectedType);
    }

    // Сортировка
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'date':
          return b.updatedAt.getTime() - a.updatedAt.getTime();
        case 'type':
          return a.type.localeCompare(b.type);
        default:
          return 0;
      }
    });

    setFilteredProjects(filtered);
  };

  const handleDeleteProject = async (projectId: string) => {
    if (confirm('Вы уверены, что хотите удалить этот проект?')) {
      try {
        await projectManager.deleteProject(projectId);
        await loadProjects();
        await loadStats();
      } catch (error) {
        console.error('Error deleting project:', error);
      }
    }
  };

  const handleForkProject = async (project: Project) => {
    try {
      const forkedName = `${project.name} (копия)`;
      await projectManager.forkProject(project.id, forkedName);
      await loadProjects();
    } catch (error) {
      console.error('Error forking project:', error);
    }
  };

  const handleExportProject = async (project: Project) => {
    try {
      const blob = await projectManager.exportProject(project.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${project.name}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting project:', error);
    }
  };

  const handleImportProject = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      await projectManager.importProject(file);
      await loadProjects();
      await loadStats();
    } catch (error) {
      console.error('Error importing project:', error);
      alert('Ошибка импорта проекта. Проверьте формат файла.');
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Б';
    const k = 1024;
    const sizes = ['Б', 'КБ', 'МБ'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const formatDate = (date: Date): string => {
    return new Intl.RelativeTimeFormat('ru').format(
      Math.ceil((date.getTime() - Date.now()) / (1000 * 60 * 60 * 24)),
      'day'
    );
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'website':
        return '🌐';
      case 'component':
        return '🧩';
      case 'template':
        return '📄';
      case 'experiment':
        return '🧪';
      default:
        return '📁';
    }
  };

  const projectTypes = [
    'all',
    'website',
    'component',
    'template',
    'experiment',
  ];

  return (
    <div
      className={cn('flex flex-col h-full bg-[#0D1117] text-white', className)}
    >
      {/* Header */}
      <div className='flex items-center justify-between p-6 border-b border-gray-800'>
        <div className='flex items-center space-x-4'>
          <h1 className='text-2xl font-bold'>Проекты</h1>
          {stats && (
            <div className='flex items-center space-x-4 text-sm text-gray-400'>
              <span>{stats.totalProjects} проектов</span>
              <span>{stats.totalFiles} файлов</span>
              <span>{formatFileSize(stats.totalSize)}</span>
            </div>
          )}
        </div>

        <div className='flex items-center space-x-2'>
          <button
            onClick={() => setShowStats(!showStats)}
            className='p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors'
            title='Статистика'
          >
            <Calendar className='w-4 h-4' />
          </button>

          <label className='p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors cursor-pointer'>
            <Upload className='w-4 h-4' />
            <input
              type='file'
              accept='.json'
              onChange={handleImportProject}
              className='hidden'
            />
          </label>

          <button
            onClick={onProjectCreate}
            className='flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors'
          >
            <Plus className='w-4 h-4 mr-2' />
            Создать
          </button>
        </div>
      </div>

      {/* Stats Panel */}
      <AnimatePresence>
        {showStats && stats && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className='border-b border-gray-800 p-6 bg-gray-900/50'
          >
            <div className='grid grid-cols-2 md:grid-cols-4 gap-4 mb-4'>
              {Object.entries(stats.projectsByType).map(([type, count]) => (
                <div key={type} className='bg-gray-800 rounded-lg p-3'>
                  <div className='flex items-center space-x-2'>
                    <span className='text-lg'>{getTypeIcon(type)}</span>
                    <div>
                      <div className='text-sm text-gray-400 capitalize'>
                        {type}
                      </div>
                      <div className='text-lg font-semibold'>{count}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className='text-sm text-gray-400'>
              Активность за последние 7 дней:
              <div className='flex items-end space-x-1 mt-2'>
                {stats.recentActivity.map(({ date, count }) => (
                  <div
                    key={date}
                    className='bg-blue-600 rounded-sm'
                    style={{
                      height: `${Math.max(count * 4, 2)}px`,
                      width: '12px',
                    }}
                    title={`${date}: ${count} проектов`}
                  />
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Filters */}
      <div className='flex items-center justify-between p-6 border-b border-gray-800'>
        <div className='flex items-center space-x-4'>
          <div className='relative'>
            <Search className='absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400' />
            <input
              type='text'
              placeholder='Поиск проектов...'
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className='pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none'
            />
          </div>

          <select
            value={selectedType}
            onChange={e => setSelectedType(e.target.value)}
            className='px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none'
          >
            {projectTypes.map(type => (
              <option key={type} value={type}>
                {type === 'all' ? 'Все типы' : type}
              </option>
            ))}
          </select>
        </div>

        <select
          value={sortBy}
          onChange={e => setSortBy(e.target.value as any)}
          className='px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none'
        >
          <option value='date'>По дате</option>
          <option value='name'>По имени</option>
          <option value='type'>По типу</option>
        </select>
      </div>

      {/* Projects Grid */}
      <div className='flex-1 overflow-y-auto p-6'>
        {isLoading ? (
          <div className='text-center text-gray-400 py-12'>
            Загрузка проектов...
          </div>
        ) : filteredProjects.length === 0 ? (
          <div className='text-center text-gray-400 py-12'>
            {searchQuery ? 'Проекты не найдены' : 'Нет проектов'}
          </div>
        ) : (
          <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
            <AnimatePresence>
              {filteredProjects.map(project => (
                <motion.div
                  key={project.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className='bg-gray-800 border border-gray-700 rounded-lg overflow-hidden hover:border-blue-500/50 transition-colors group'
                >
                  {/* Project Header */}
                  <div className='p-4 border-b border-gray-700'>
                    <div className='flex items-start justify-between'>
                      <div className='flex-1 min-w-0'>
                        <div className='flex items-center space-x-2 mb-1'>
                          <span className='text-lg'>
                            {getTypeIcon(project.type)}
                          </span>
                          <h3 className='font-semibold truncate'>
                            {project.name}
                          </h3>
                        </div>
                        <p className='text-sm text-gray-400 line-clamp-2'>
                          {project.metadata.description || 'Без описания'}
                        </p>
                      </div>

                      <div className='ml-2 opacity-0 group-hover:opacity-100 transition-opacity'>
                        <div className='flex items-center space-x-1'>
                          <button
                            onClick={() => onProjectSelect?.(project)}
                            className='p-1 text-gray-400 hover:text-white hover:bg-gray-700 rounded'
                            title='Открыть'
                          >
                            <Eye className='w-3 h-3' />
                          </button>
                          <button
                            onClick={() => handleForkProject(project)}
                            className='p-1 text-gray-400 hover:text-white hover:bg-gray-700 rounded'
                            title='Копировать'
                          >
                            <Copy className='w-3 h-3' />
                          </button>
                          <button
                            onClick={() => handleExportProject(project)}
                            className='p-1 text-gray-400 hover:text-white hover:bg-gray-700 rounded'
                            title='Экспорт'
                          >
                            <Download className='w-3 h-3' />
                          </button>
                          <button
                            onClick={() => handleDeleteProject(project.id)}
                            className='p-1 text-gray-400 hover:text-red-400 hover:bg-gray-700 rounded'
                            title='Удалить'
                          >
                            <Trash2 className='w-3 h-3' />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Project Info */}
                  <div className='p-4'>
                    <div className='flex items-center justify-between text-xs text-gray-400 mb-3'>
                      <span>{formatDate(project.updatedAt)}</span>
                      <span>v{project.version}</span>
                    </div>

                    <div className='flex items-center space-x-4 text-xs text-gray-500 mb-3'>
                      <span className='flex items-center'>
                        <FileText className='w-3 h-3 mr-1' />
                        {project.files.length}
                      </span>
                      <span className='flex items-center'>
                        <Clock className='w-3 h-3 mr-1' />
                        {project.metadata.estimatedTime}мин
                      </span>
                    </div>

                    {project.metadata.tags.length > 0 && (
                      <div className='flex flex-wrap gap-1'>
                        {project.metadata.tags.slice(0, 3).map(tag => (
                          <span
                            key={tag}
                            className='px-2 py-1 bg-gray-700 text-xs rounded text-gray-300'
                          >
                            {tag}
                          </span>
                        ))}
                        {project.metadata.tags.length > 3 && (
                          <span className='text-xs text-gray-500'>
                            +{project.metadata.tags.length - 3}
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );
}
