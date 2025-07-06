'use client';

import ProjectManagerSimple from '@/components/projects/ProjectManagerSimple';
import { Project } from '@/lib/project-manager';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';

export default function ProjectsPage() {
  const router = useRouter();

  const handleProjectSelect = (project: Project) => {
    // Открываем проект в генераторе
    router.push(`/generator?project=${project.id}`);
  };

  const handleProjectCreate = () => {
    // Создаем новый проект в генераторе
    router.push('/generator?new=true');
  };

  return (
    <div className='min-h-screen bg-[#0D1117] text-white'>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className='h-screen'
      >
        <ProjectManagerSimple
          onProjectSelect={handleProjectSelect}
          onProjectCreate={handleProjectCreate}
        />
      </motion.div>
    </div>
  );
}
